import pandas as pd
import lightgbm as lgb

def preprocess_data(df_train:pd.DataFrame, columns_to_remove):
    X = [x for x in df_train.columns if "target" not in x and "instance" not in x]
 
    # train data features
    X_train = df_train[X]
    X_train = X_train.drop(columns_to_remove, axis = 1)

    # train data targets
    y_train_memory = df_train["target_memory"]

    return X_train, y_train_memory


def get_low_feature_importance(df_train:pd.DataFrame):
    X = [x for x in df_train.columns if "target" not in x and "instance" not in x]

    # train data features
    X_train = df_train[X]

    # train data targets
    y_train_cpu = df_train["target_cpu"]
    y_train_network = df_train["target_network"]
    y_train_memory = df_train["target_memory"]

    # intialize all models
    lgb_cpu = lgb.LGBMRegressor()
    lgb_network = lgb.LGBMRegressor()
    lgb_memory = lgb.LGBMRegressor()

    # train on CPU
    lgb_cpu.fit(X_train, y_train_cpu)

    # train on memory
    lgb_memory.fit(X_train, y_train_memory)

    # train on network
    lgb_network.fit(X_train, y_train_network)

    # get feature importance for every target
    importance_cpu = pd.DataFrame({"features":X, "Importance":lgb_cpu.feature_importances_}).sort_values("Importance", ascending=False)
    importance_network  = pd.DataFrame({"features":X, "Importance":lgb_network.feature_importances_}).sort_values("Importance", ascending=False)
    importance_memory = pd.DataFrame({"features":X, "Importance":lgb_memory.feature_importances_}).sort_values("Importance", ascending=False)

    low_feature_importance_columns = []
    # get all low feature importance 
    low_feature_importance_columns.extend(importance_cpu.loc[importance_cpu.Importance < 25, "features"].values)
    low_feature_importance_columns.extend(importance_network.loc[importance_network.Importance < 25, "features"].values)
    low_feature_importance_columns.extend(importance_memory.loc[importance_memory.Importance < 25, "features"].values)

    # # only mark features as low importance if it exists across all three groups
    low_feature_importance_columns = pd.DataFrame({"low_importance":low_feature_importance_columns})
    low_feature_importance_columns = low_feature_importance_columns.groupby("low_importance").size() == 3
    low_feature_importance_columns = list(low_feature_importance_columns[low_feature_importance_columns].index)
    low_feature_importance_columns_dl = [x for x in low_feature_importance_columns if "instance" not in x]

    return low_feature_importance_columns, low_feature_importance_columns_dl