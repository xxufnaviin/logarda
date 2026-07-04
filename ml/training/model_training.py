# train time series forecasting models
import pandas as pd 
import warnings
import json

from ml.data.prepare import prepare_data
from ml.training.gru import model as gru
from ml.training.lightgbm import model as lightgbm
from ml.training.linear import model as linear
from ml.training.lightgbm.preprocess import get_low_feature_importance

warnings.filterwarnings("ignore")

def train_time_series_models():
    # prepare data for model training
    df_train, df_validate, df_test = prepare_data(data_type="train")

    # get low importance feature columns to remove
    lightgbm_cols, gru_columns = get_low_feature_importance(df_train)

    # train both gru model and lightgbm model
    features_gru = gru.train_and_save(df_train, df_validate, df_test, remove_cols=gru_columns)
    features_lgb = lightgbm.train_and_save(df_train, df_validate, df_test, remove_cols=lightgbm_cols)
    linear.train_and_save(df_train, df_validate, df_test, remove_cols=lightgbm_cols)


    with open("ml/artifacts/features/features.json", "w") as file:
        json.dump({
            "gru":features_gru,
            "lgb":features_lgb
        }, file)


if __name__ == "__main__":
    train_time_series_models()