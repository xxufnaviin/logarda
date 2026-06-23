# not endpoint, modular functions just to expose the models
from ml.data.prepare import prepare_data, prepare_prediction_data
from ml.inference.gru.model import gru_predict

def predict(username:str):
    df_original = prepare_data("predict", username)

    
    print(df_original)
    for instance_group, df_instance in df_original.groupby("instanceid"):
        print(instance_group)

        gru_predict(df_instance)
        break

    # add logic to iterate through each instance and predict 13 data points (minus one since og data has it)
    # then concat back to the dataframe by adding time (5 min interval) and its values
    # inverse transform the instance group and username and put it back to og dataset, then filter out predicted metrics to return


predict("xxufnaviin")
