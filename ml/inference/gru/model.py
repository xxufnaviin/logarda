import joblib 
import pandas as pd
import json
from datetime import datetime, timezone, timedelta

from ml.inference.gru.preprocess import preprocess_data, create_predicted_row
from ml.data.prepare import prepare_prediction_data

def gru_predict(df_original:pd.DataFrame):
    features = get_features()
    model = get_model()

    df_predict = prepare_prediction_data(df_original)
    last_timestamp = df_predict.index[-1]
    predicted_timestamp = last_timestamp + timedelta(minutes=5) # first predicted timestamp

    predicted_dataframe = pd.DataFrame()

    for _ in range (14):
        # create nn dataset
        df_predict = prepare_prediction_data(df_original)
        # print(df_predict.tail(12))
        predict_dataset = preprocess_data(df_predict.tail(12), features)
        results = model.predict(predict_dataset) # make prediction
        
        # get predicted row
        predicted_row = create_predicted_row(results, predicted_timestamp)

        # concat into original dataframe to get rolling features
        df_original = pd.concat([predicted_row, df_original],ignore_index=True)
        
        df_original = df_original.bfill()
        predicted_dataframe = pd.concat([predicted_dataframe, predicted_row], ignore_index=True)

        predicted_timestamp = predicted_timestamp + timedelta(minutes=5)
    
    # fill na in predicted dataframe
    predicted_dataframe['instanceid'] = df_original["instanceid"][0]
    predicted_dataframe['username'] = df_original["username"][0]

    # should only return starting from 2nd row, since the first row already has actual value
    # but for feed forward prediction of data, need to include back at least five previous values
    idx = df_original.index[df_original["metrictime"] == last_timestamp][0]
    history = df_original.iloc[idx-1:idx+10].sort_values("metrictime")

    results =  pd.concat([history, predicted_dataframe[1:]],ignore_index=True).reset_index(drop=True)

    print(results)
    return results



def get_model():
    return joblib.load("ml/artifacts/models/gru_model.pkl")

def get_features():
    with open("ml/artifacts/features/features.json", "r") as file:
        features = json.load(file)

    return features['gru']