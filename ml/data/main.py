from load import *
from pipeline import *


def prepare_data(data_type:str, username = None):
    if data_type == "train":
        df = load_data(data_type)
        df_train, df_validate, df_test = processing_pipeline(df, data_type)

        print(df_train.head(5))

    elif data_type == "predict":
        df = load_data(data_type,"xxufnaviin")
        df_predict = processing_pipeline(df, data_type)
    
        print(df_predict)


prepare_data("predict")