# only used for predicting memory
import pandas as pd
import lightgbm as lgb
import joblib

from ml.training.lightgbm.preprocess import preprocess_data

def train_and_save(df_train:pd.DataFrame, df_validate:pd.DataFrame, df_test:pd.DataFrame, remove_cols):
    # preprocess data
    X, y = preprocess_data(df_train, remove_cols)

    # fit model onto X and Y
    model = train_model(X,y)

    # save model
    save_model(model)

    return list(X.columns)

def train_model(X, y):
    lgb_memory = lgb.LGBMRegressor()

    # train on memory
    lgb_memory.fit(X, y)

    return lgb_memory


def save_model(model):
    # save model in artifacts
    joblib.dump(model, "ml/artifacts/models/lgb_memory.pkl")

