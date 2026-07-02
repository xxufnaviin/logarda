from fastapi import FastAPI
import uvicorn

from routers import analytics
from routers import performance

analyticsAPI = FastAPI()
analyticsAPI.include_router(analytics.router, prefix="/api/analytics")
analyticsAPI.include_router(performance.router, prefix="/api/models")


@analyticsAPI.get("/api")
def get_health():
    return {
        "message": "API running",
        "status": 200    
    }

if __name__ == "__main__":
    uvicorn.run("main:analyticsAPI", host="localhost", port=8000)
