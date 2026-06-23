from ml.data.load import *
from ml.data.pipeline import *


def prepare_data(data_type:str, username = None):
    if data_type == "train":
        df = load_data(data_type)
        df_train, df_validate, df_test = processing_pipeline(df, data_type)

        return df_train, df_validate, df_test

    elif data_type == "predict":
        return load_data(data_type,username)

def prepare_prediction_data(df_original:pd.DataFrame):
    df = df_original.copy()
    df_predict = processing_pipeline(df, "predict")

    return df_predict 

# prepare_data("predict","xxufnaviin")