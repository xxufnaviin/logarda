import joblib 
import pandas as pd
import json
from datetime import  timedelta




def predict(df_predict:pd.DataFrame):
    # features = get_features()
    # model = get_model()

    last_timestamp = df_predict.index[-1]
    predicted_timestamp = last_timestamp + timedelta(minutes=5) # first predicted timestamp


def get_model():
    return joblib.load("ml/artifacts/models/lgb_memory.pkl")

def get_features():
    with open("ml/artifacts/features/features.json", "r") as file:
        features = json.load(file)

    return features['lgb']