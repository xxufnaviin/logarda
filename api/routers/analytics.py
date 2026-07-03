from fastapi import APIRouter, Depends
import time
import json

from api.utils.helper import *
from utils.utils import sha256_hash
from ml.inference.predictor import predict
from llm.inference import generate_explanation
from api.models.analytics import MetricsPredictionRequest, LLMInferenceRequest

router = APIRouter()

@router.get("/predict")
def get_prediction(request:MetricsPredictionRequest = Depends()):
    if not request.username or not request.duration: 
        return { 
            "message": "Request parameters incomplete. Please include BOTH username and duration.", 
            "status": "Failed" 
        }
    
    for results, err in predict(request.username, hours=request.duration):
        if err:
            return {
                "message": "No records found for user. No predictions have been made",
                "status": "Failed"
            }
        push_predicted_metrics(results)
        time.sleep(0.5)
    
    return {
        "message": "Prediction results have been pushed to message queue.",
        "status": "Success"
    }

@router.post("/llm/inference")
def get_error_explanation(request:LLMInferenceRequest):
    # form rag query from request, only using keywords for simpler query without noise
    # example: InternalFailure in EC2 / AccessDenied in S3
    rag_query = generate_rag_query(request.errorCode, request.serviceName)
    query = generate_query(request.errorCode, request.serviceName, request.eventName, request.errorMessage)

    # generate hash key based on errorcode, service and event name
    hash_key = f"kvcache:{sha256_hash(f'{request.errorCode}{request.serviceName}{request.eventName}')}"

    # if value is cached then no get results 
    results, ok = check_kv_cache(hash_key)
    if ok:
        result = json.loads(results)
        return result

    # get llm results and append it to kv cache
    results = generate_explanation(query, rag_query)
    append_kv_cache(hash_key, json.dumps(results))

    return results