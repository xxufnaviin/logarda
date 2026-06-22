# not endpoint, modular functions just to expose the models
from ml.data.prepare import prepare_data


import joblib

le = joblib.load("ml/artifacts/scalers/label_encoder.pkl")



def predict(username:str):
    df_original, df_predict = prepare_data("predict", username)

    # print(df_original)
    print(df_predict)
    for instance_group, df_instance in df_predict.groupby("instance_group"):
        print(instance_group)
        print(df_instance.tail(12)) # get last 12 values for neural network

    # add logic to iterate through each instance and predict 13 data points (minus one since og data has it)
    # then concat back to the dataframe by adding time (5 min interval) and its values
    # inverse transform the instance group and username and put it back to og dataset, then filter out predicted metrics to return


predict("xxufnaviin")
