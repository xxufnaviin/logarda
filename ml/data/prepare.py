from ml.data.load import *
from ml.data.pipeline import *


def prepare_data(data_type:str, username = None):
    if data_type == "train":
        df = load_data(data_type)
        df_train, df_validate, df_test = processing_pipeline(df, data_type)

        return df_train, df_validate, df_test

    elif data_type == "predict":
        df = load_data(data_type,username)
        df_original = df.copy()
        
        df_predict = processing_pipeline(df, data_type)

        return df_original, df_predict


# prepare_data("predict","xxufnaviin")