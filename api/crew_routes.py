from fastapi import APIRouter, HTTPException
from crew.retail_crew import run_retail_crew
from schemas.crew_schema import RetailRequest
from database import retail_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter()


@router.post("/crew/analyze")
async def analyze(data: RetailRequest):

    result = await run_retail_crew(
        total_sales=data.total_sales,
        monthly_growth=data.monthly_growth,
        top_category=data.top_category
    )

    doc = {
        "total_sales": data.total_sales,
        "monthly_growth": data.monthly_growth,
        "top_category": data.top_category,

        # auto-generated
        "ai_analysis": result,
        "created_at": datetime.utcnow()
    }

    inserted = await retail_collection.insert_one(doc)

    return {
        "status": "success",
        "id": str(inserted.inserted_id),
        "analysis": result
    }


@router.get("/crew/history")
async def history():

    result=[]

    cursor=retail_collection.find()

    async for item in cursor:
        item["_id"]=str(item["_id"])
        result.append(item)

    return result


