# train time series forecasting models
from ml.data.prepare import prepare_data
from ml.training.gru import model as gru
from ml.training.lightgbm import model as lightgbm

def train_time_series_models():
    # prepare data for model training
    df_train, df_validate, df_test = prepare_data(data_type="train")

    # train both gru model and lightgbm model
    gru.train_and_save(df_train, df_validate, df_test)
    lightgbm.train_and_save(df_train, df_validate, df_test)