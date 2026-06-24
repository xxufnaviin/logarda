from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone

from utils.redis import *
from ml.inference.predictor import predict

router = APIRouter()
r = Redis.create_connection()

if config.secrets.ENVIRONMENT == "PRD":
    PREDICTED_METRICS_STREAM = "predicted_metrics"
else:
    PREDICTED_METRICS_STREAM = "stg_predicted_metrics"

@router.get("/predict")
def get_prediction(username: str, duration: int):
    if not username or not duration: 
        return { 
            "message": "Request parameters incomplete. Please include BOTH username and duration.", 
            "status": "Failed" 
        }
    
    for results, err in predict(username, hours=duration):
        if err:
            return {
                "message": "No records found for user. No predictions have been made",
                "status": "Failed"
            }
        print(results)
        push_predicted_metrics(results)
    
    return {
        "message": "Prediction results have been pushed to message queue.",
        "status": "Success"
    }


def push_predicted_metrics(results):
    for _, row in results.iterrows():
        message = row.to_dict()
        message["metrictime"] = datetime.strptime(message["metrictime"].strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        message["metrictime"] = message["metrictime"].isoformat()

        Redis.enqueue_message(r, PREDICTED_METRICS_STREAM, message)
