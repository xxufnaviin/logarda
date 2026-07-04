from pydantic import BaseModel
from datetime import datetime


class MetricsPredictionRequest(BaseModel):
    username:str
    duration:int

class LLMInferenceRequest(BaseModel):
    eventTime:datetime 
    errorCode:str
    errorMessage:str 
    serviceName:str 
    eventName:str 
    username:str 

class LLMInferenceUserRequest(BaseModel):
    query:str
