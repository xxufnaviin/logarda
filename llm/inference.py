from llm.vectordb.client import ChromaDB
from llm.client import LLM

ChromaDB.init_client()
LLM.init_client()


def generate_explanation(query:str, rag_query:str = None):
    # get rag query
    if rag_result:
        rag_result = ChromaDB.query(rag_query)

    # feed into LLM
    error_explanation, ok = LLM.generate_text(query, rag_result)
    if ok:
        return {
            "data":{
                "explanation":error_explanation["explanation"],
                "solution": error_explanation["solution"]
            },
            "status": 200
        }
    
    ## fallback to string only explanation
    return {
        "data": {
            "explanation":error_explanation
        },
        "status": 200
    }
        