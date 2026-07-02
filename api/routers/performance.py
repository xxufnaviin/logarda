from fastapi import APIRouter
from utils.utils import load_model_performance_from_JSON, load_gru_performance_from_JSON

router = APIRouter()


@router.get("/all/performance")
def get_model_performance():
    data = load_model_performance_from_JSON()

    print("Model performance have been successfully fetched for all models.")
    return(data)

@router.get("/gru/performance")
def get_model_performance():
    data = load_gru_performance_from_JSON()

    print("GRU training performance have been successfully fetched.")
    return(data)
