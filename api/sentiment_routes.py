from fastapi import APIRouter
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os

load_dotenv()

router=APIRouter()

endpoint=os.getenv("AZURE_LANGUAGE_ENDPOINT")
key=os.getenv("AZURE_LANGUAGE_KEY")

client=TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

history=[]

@router.post("/sentiment-agent/analyze")
def analyze(data:dict):

    review=data["review"]

    response=client.analyze_sentiment(
        documents=[review]
    )[0]

    result={
        "review":review,
        "sentiment":response.sentiment,
        "confidence":response.confidence_scores.positive
    }

    history.append(result)

    return result


@router.get("/sentiment-agent/history")
def get_history():
    return history