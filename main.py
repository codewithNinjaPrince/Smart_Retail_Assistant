from fastapi import FastAPI
from api.anomaly_api import router as anomaly_router
from api.demand_api import router as demand_router
from api.rag_api import router as rag_router
from api.document_routes import router as document_router
from api.sentiment_routes import router as sentiment_router
from api.crew_routes import router as crew_router

app=FastAPI(
    title="Retail Multi-Agent System"
)

@app.get("/")
def home():
    return {"message":"Welcome to the Retail Multi-Agent System API, Go to /docs for the API documentation"}

app.include_router(
    anomaly_router,
)

app.include_router(
    demand_router,
)

app.include_router(
    rag_router
)

app.include_router(
    document_router
)

app.include_router(sentiment_router)

app.include_router(crew_router)