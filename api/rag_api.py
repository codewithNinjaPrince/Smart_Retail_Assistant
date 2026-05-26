from fastapi import APIRouter
from rag.chat import ask_rag
from database import chat_collection
from schemas.rag_schema import QueryRequest


router = APIRouter(
    prefix="/data-analyst-and-query-agent",
    tags=["RAG AI Agent"]
)


@router.post("/ask")
async def ask_sales_insights(data: QueryRequest):

    """
    Ask questions related to retail sales insights,
    products, trends, profits, demand, inventory etc.
    """

    response = await ask_rag(
        data.query
    )

    return {

        "agent": "ML Insight Agent",
        "query": data.query,
        "answer": response,
        "message":
        "Ask anything about retail sales data, demand, trends, products or insights.",
    }


@router.get("/history")
async def get_insight_history():

    data=[]

    cursor = chat_collection.find().sort(
        "createdAt",
        -1
    ).limit(5)


    async for item in cursor:

        item["_id"] = str(
            item["_id"]
        )

        data.append(item)

    return {

        "agent":"ML Insight Agent",

        "description":
        "Recent sales insight conversations",

        "count":len(data),

        "history":data
    }