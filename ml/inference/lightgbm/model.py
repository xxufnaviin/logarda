import joblib 
import pandas as pd
import json
from datetime import datetime, timezone, timedelta

from ml.inference.lightgbm.preprocess import preprocess_data, get_memory_value,create_predicted_row
from ml.data.prepare import prepare_prediction_data


def lgb_predict(df_original:pd.DataFrame, hours:int, predicted_df:pd.DataFrame):
    features = get_features()
    model = get_model()

    df_predict = prepare_prediction_data(df_original)
    last_timestamp = df_predict.index[-1]
    predicted_timestamp = last_timestamp + timedelta(minutes=5) # first predicted timestamp
    horizon = hours * 12 + 2

    for i in range (horizon):
        # create row for prediction
        df_predict = prepare_prediction_data(df_original)
        X_predict = preprocess_data(df_predict[-1:], features)

        # make prediction and get original value
        results =  model.predict(X_predict)
        results = get_memory_value(results)

        if i == 0:
            # get predicted row
            predicted_row = create_predicted_row(results, predicted_timestamp)

            # concat into original dataframe to get rolling features
            df_original = pd.concat([predicted_row, df_original],ignore_index=True)
            
            df_original = df_original.bfill()

        else:
            # update predicted dataframe
            predicted_df.loc[predicted_df["metrictime"] == predicted_timestamp, "memory"] = results

            # get the row
            predicted_row = predicted_df.loc[predicted_df["metrictime"] == predicted_timestamp]

            # concat into original dataframe to get rolling features
            df_original = pd.concat([predicted_row, df_original],ignore_index=True)

        predicted_timestamp = predicted_timestamp + timedelta(minutes=5)    
    
    return predicted_df

def get_model():
    return joblib.load("ml/artifacts/models/lgb_memory.pkl")

def get_features():
    with open("ml/artifacts/features/features.json", "r") as file:
        features = json.load(file)

    return features['lgb']