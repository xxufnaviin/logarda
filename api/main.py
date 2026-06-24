from fastapi import FastAPI
from routers import analytics
import uvicorn

analyticsAPI = FastAPI()
analyticsAPI.include_router(analytics.router, prefix="/api/analytics")


@analyticsAPI.get("/api")
def get_health():
    return {
        "message": "API running",
        "status": 200    
    }

if __name__ == "__main__":
    uvicorn.run("main:analyticsAPI", host="localhost", port=8000)
