import pandas as pd
import numpy as np
from config.secrets import *

from ml.data.preprocessing.feature_scaling import feature_scale_data, feature_scale_dataset
from ml.data.preprocessing.data_split import train_val_test_split
from ml.data.preprocessing.clean_dataset import clean_dataset
from ml.data.preprocessing.data_transformation import preprocess_data, preprocess_dataset

import warnings

warnings.filterwarnings("ignore")

def processing_pipeline(df:pd.DataFrame, type:str):
    df = clean_dataset(df)

    if type == "train":
        df_train, df_validate, df_test = train_val_test_split(df)
        df_train, df_validate, df_test = preprocess_dataset(df_train, df_validate, df_test)
        df_train, df_validate, df_test = feature_scale_dataset(df_train, df_validate, df_test)

        return df_train, df_validate, df_test
    
    elif type == "predict":
        df_predict = preprocess_data(df)
        df_predict = feature_scale_data(df_predict)

        return df_predict
    







