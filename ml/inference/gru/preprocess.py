import json
import pandas as pd
import numpy as np
import joblib

from keras.preprocessing import timeseries_dataset_from_array
from ml.data.preprocessing.feature_scaling import feature_scale_data

def inverse_transform(results):
    scaler_y = joblib.load("ml/artifacts/scalers/standard_scaler_y.pkl")

    results = scaler_y.inverse_transform(results)
    results = np.expm1(results)
    
    return results

def create_predicted_row(results, time):
    print(results[0])
    results = inverse_transform(results)
    row = {
        "metrictime": time,
        "instanceid": pd.NA,
        "cpu": results[0][0],
        "network": results[0][2],
        "memory": results[0][1],
        "username": pd.NA

    }
    print(results[0])
    return pd.DataFrame([row])



def preprocess_data(df_predict, features):
    predict_data = df_predict[features].values
    print("prepocess",features)
    lookback = 12 # how many steps to look back, 12 for 5-minute itnervals is 1 hour roughly

    predict_X = predict_data
    predict_X = predict_X.astype(np.float32)


    prediction_dataset = timeseries_dataset_from_array(
    data=predict_X,
    targets=None,
    sequence_length=lookback,
    batch_size=32
    )

    return prediction_dataset