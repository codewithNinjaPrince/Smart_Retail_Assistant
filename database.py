from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client=AsyncIOMotorClient(
    os.getenv("MONGO_URI")
)

db=client[
    os.getenv("DB_NAME")
]

chat_collection=db.chat_history

document_collection=db["documents"]

retail_collection = db["crew_analysis"]