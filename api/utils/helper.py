from datetime import datetime, timezone

from utils.redis import *

r = Redis.create_connection()

if config.secrets.ENVIRONMENT == "PRD":
    PREDICTED_METRICS_STREAM = "predicted_metrics"
else:
    PREDICTED_METRICS_STREAM = "stg_predicted_metrics"


def push_predicted_metrics(results):
    for _, row in results.iterrows():
        message = row.to_dict()
        message["metrictime"] = datetime.strptime(message["metrictime"].strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        message["metrictime"] = message["metrictime"].isoformat()
        print(message)
        Redis.enqueue_message(r, PREDICTED_METRICS_STREAM, message)

def append_kv_cache(key:str, value:str):
    # append to cache
    Redis.set_key(r, key, value)

def check_kv_cache(key:str):
    # check if key exist
    value = Redis.get_key(key)
    if value:
        return value, True
    else:
        return "", False
    
def generate_query(errorCode, serviceName, eventName, errorMsg):
    return f"Encountered {errorCode} in {serviceName}, while doing the operation {eventName}. Error message given was {errorMsg}."

def generate_rag_query(errorCode, serviceName):
    return f"{errorCode} in {serviceName}"