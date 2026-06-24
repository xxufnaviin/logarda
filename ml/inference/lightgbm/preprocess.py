import json
import pandas as pd
import numpy as np
import joblib

def inverse_transform(results):
    scaler_y = joblib.load("ml/artifacts/scalers/standard_scaler_y.pkl")

    results = scaler_y.inverse_transform(results)
    results = np.expm1(results)

    print(f"{results[0][1]:.2f}")
    return results

def get_memory_value(results):
    # simulate cpu and network for inverse transform
    results = [[0, results[0], 0]]
    results = inverse_transform(results)

    return results[0][1]

def create_predicted_row(results, time):
    row = {
        "metrictime": time,
        "instanceid": pd.NA,
        "cpu": pd.NA,
        "network": pd.NA,
        "memory": results,
        "username": pd.NA

    }
    return pd.DataFrame([row])

def preprocess_data(df_predict, features):
    # train data features
    return df_predict[features]

