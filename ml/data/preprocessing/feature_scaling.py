from sklearn.preprocessing import RobustScaler, LabelEncoder, OneHotEncoder
import joblib
import pandas as pd
import numpy as np

def feature_scale_dataset(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame):
    df_train, df_validate, df_test = logarize_dataset(df_train, df_validate, df_test)
    df_train, df_validate, df_test = standardize_dataset(df_train, df_validate, df_test)
    
    return df_train, df_validate, df_test

## for prediction pipeline
def feature_scale_data(df_predict:pd.DataFrame):
    df_predict = logarize_data(df_predict)
    df_predict = standardize_data(df_predict)

    return df_predict


## helper functions
def label_encode_dataset(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame):
    le = LabelEncoder() # label encode for tree-based models
    df_train["instance_group"] = le.fit_transform(df_train["instance_group"])
    df_test["instance_group"] = le.transform(df_test["instance_group"])
    df_validate["instance_group"] = le.transform(df_validate["instance_group"])

    joblib.dump(le, "ml/artifacts/scalers/label_encoder.pkl")

    return df_train, df_validate, df_test

def onehot_encode_dataset(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame):
    ohe = OneHotEncoder(drop="first",handle_unknown="ignore",sparse_output=False)
    ohe.fit(df_train[["instance_group"]])

    feature_names = ohe.get_feature_names_out(["instance_group"])

    train_ohe = pd.DataFrame(ohe.transform(df_train[["instance_group"]]), columns=feature_names, index=df_train.index).astype(bool)
    test_ohe = pd.DataFrame(ohe.transform(df_test[["instance_group"]]), columns=feature_names, index=df_test.index).astype(bool)
    validate_ohe = pd.DataFrame(ohe.transform(df_validate[["instance_group"]]), columns=feature_names, index=df_validate.index).astype(bool)

    df_train = pd.concat([df_train, train_ohe], axis=1)
    df_test = pd.concat([df_test, test_ohe], axis=1)
    df_validate = pd.concat([df_validate, validate_ohe], axis=1)

    joblib.dump(ohe, "ml/artifacts/scalers/onehot_encoder.pkl")

    return df_train, df_validate, df_test

def signed_log(x):
    return np.sign(x) * np.log1p(np.abs(x))

def logarize_dataset(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame):
    df_numerical_train_test = get_numerical_features(df_train)
    df_train[df_numerical_train_test] = df_train[df_numerical_train_test].apply(signed_log)
    df_test[df_numerical_train_test] = df_test[df_numerical_train_test].apply(signed_log)
    df_validate[df_numerical_train_test] = df_validate[df_numerical_train_test].apply(signed_log)

    return df_train, df_validate, df_test

def standardize_dataset(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame):
    scaler = RobustScaler()
    scaler_y = RobustScaler()
    exclude_scaling = get_excluded_features_standarization(df_train)
    target = ["target_cpu", "target_memory", "target_network"]
    time = ["hour", "day", "day_of_week", "minute"]

    # train data is fitted on normalization scaler
    scaled_data = pd.DataFrame(scaler.fit_transform(df_train.drop(columns=exclude_scaling, axis=1)), 
                    columns = scaler.get_feature_names_out(), index=df_train.index) 

    df_train = pd.concat([scaled_data,df_train[exclude_scaling]], axis=1)

    # test data using same scaler
    scaled_data = pd.DataFrame(scaler.transform(df_test.drop(columns=exclude_scaling, axis=1)), 
                    columns = scaler.get_feature_names_out(), index=df_test.index) 

    df_test = pd.concat([scaled_data,df_test[exclude_scaling]], axis=1)

    # validation data using same scaler
    scaled_data = pd.DataFrame(scaler.transform(df_validate.drop(columns=exclude_scaling, axis=1)), 
                    columns = scaler.get_feature_names_out(), index=df_validate.index) 

    df_validate = pd.concat([scaled_data,df_validate[exclude_scaling]], axis=1)

    # target variables (train)
    scaled_y = pd.DataFrame(scaler_y.fit_transform(df_train[target]), 
                        columns = scaler_y.get_feature_names_out(), index=df_train.index)

    df_train = df_train.drop(target, axis = 1)
    df_train = pd.concat([scaled_y, df_train], axis = 1 )      

    # test data
    scaled_y = pd.DataFrame(scaler_y.transform(df_test[target]), 
                        columns = scaler_y.get_feature_names_out(), index=df_test.index)

    df_test = df_test.drop(target, axis = 1)
    df_test = pd.concat([scaled_y, df_test], axis = 1 )      

    # validate
    scaled_y = pd.DataFrame(scaler_y.transform(df_validate[target]), 
                        columns = scaler_y.get_feature_names_out(), index=df_validate.index)

    df_validate = df_validate.drop(target, axis = 1)
    df_validate = pd.concat([scaled_y, df_validate], axis = 1 )     

    joblib.dump(scaler, "ml/artifacts/scalers/standard_scaler.pkl")
    joblib.dump(scaler_y, "ml/artifacts/scalers/standard_scaler_y.pkl")

    return df_train, df_validate, df_test


## for prediction
def label_encode_data(df_predict:pd.DataFrame): # for prediction dataset
    le = joblib.load("ml/artifacts/scalers/label_encoder.pkl")
    df_predict["instance_group"] = le.transform(df_predict["instance_group"])

    return df_predict

def onehot_encode_data(df_predict:pd.DataFrame):
    ohe = joblib.load("ml/artifacts/scalers/onehot_encoder.pkl")
    feature_names = ohe.get_feature_names_out(["instance_group"])

    predict_ohe = pd.DataFrame(ohe.transform(df_predict[["instance_group"]]), columns=feature_names, index=df_predict.index).astype(bool)
    df_predict = pd.concat([df_predict, predict_ohe], axis=1)

    return df_predict

def logarize_data(df_predict:pd.DataFrame):
    df_numerical_train_test = get_numerical_features(df_predict)
    df_predict[df_numerical_train_test] = df_predict[df_numerical_train_test].apply(signed_log)

    return df_predict

def standardize_data(df_predict:pd.DataFrame):
    scaler = joblib.load("ml/artifacts/scalers/standard_scaler.pkl")
    scaler_y = joblib.load("ml/artifacts/scalers/standard_scaler_y.pkl")
    exclude_scaling = get_excluded_features_standarization(df_predict)
    target = ["target_cpu", "target_memory", "target_network"]
    time = ["hour", "day", "day_of_week", "minute"]

    # predict data using same scaler
    scaled_data = pd.DataFrame(scaler.transform(df_predict.drop(columns=exclude_scaling, axis=1)), 
                    columns = scaler.get_feature_names_out(), index=df_predict.index) 

    df_predict = pd.concat([scaled_data,df_predict[exclude_scaling]], axis=1)

    # test data
    scaled_y = pd.DataFrame(scaler_y.transform(df_predict[target]), 
                        columns = scaler_y.get_feature_names_out(), index=df_predict.index)

    df_predict = df_predict.drop(target, axis = 1)
    df_predict = pd.concat([scaled_y, df_predict], axis = 1 )  

    return df_predict

# utils function
def get_excluded_features_standarization(df_train:pd.DataFrame):
    exclude = list(df_train.select_dtypes(exclude=np.number).columns)
    exclude.remove("instance_group")
    return exclude + ["target_cpu", "target_memory", "target_network", "instance_group"]

def get_numerical_features(df_train:pd.DataFrame):
    df_numerical_train_test = list(df_train.select_dtypes(include=np.number).columns) 
    df_numerical_train_test.remove("hour")
    df_numerical_train_test.remove("day")
    df_numerical_train_test.remove("day_of_week")
    df_numerical_train_test.remove("minute")
    # df_numerical_train_test.remove("instance_group")

    return df_numerical_train_test