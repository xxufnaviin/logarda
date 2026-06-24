# not endpoint, modular functions just to expose the models
from ml.data.prepare import prepare_data
from ml.inference.gru.model import gru_predict
from ml.inference.lightgbm.model import lgb_predict

def predict(username:str, hours:int):
    data = prepare_data("predict", username)
    if data.empty:
        yield data, "error"
    
    for instance, instance_data in data.groupby("instanceid"):
        print("Predicting for:", instance, " by:", username)

        results = gru_predict(instance_data, hours)
        results = lgb_predict(instance_data, hours, results)
        
        yield results, None

    # add logic to iterate through each instance and predict 12*2 + 2  data points (minus one since og data has it)
    # then concat back to the dataframe by adding time (5 min interval) and its values
    # inverse transform the instance group and username and put it back to og dataset, then filter out predicted metrics to return
    # generate prediction of CPU, Network and Memory using GRU, then Feed forward to LIGHTGBM to update Memory prediction




