# not endpoint, modular functions just to expose the models
from ml.data.prepare import prepare_data, prepare_prediction_data
from ml.inference.gru.model import gru_predict

def predict(username:str):
    data = prepare_data("predict", username)
    print(data)
    for instance, instance_data in data.groupby("instanceid"):
        print("Predicting for:", instance, " by:", username)

        results = gru_predict(instance_data)
        

    # add logic to iterate through each instance and predict 13 data points (minus one since og data has it)
    # then concat back to the dataframe by adding time (5 min interval) and its values
    # inverse transform the instance group and username and put it back to og dataset, then filter out predicted metrics to return


predict("xxufnaviin")
