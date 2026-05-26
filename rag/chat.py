from rag.retriever import search_docs
from database import chat_collection

from datetime import datetime

from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


client=AzureOpenAI(
    api_key=os.getenv(
        "AZURE_OPENAI_KEY"
    ),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )
)


async def ask_rag(question):

    context="\n".join(
        search_docs(question)
    )


    prompt=f"""
Context:
{context}

Question:
{question}

Answer only from context.
"""


    response=client.chat.completions.create(
        model=os.getenv(
             "CHAT_DEPLOYMENT"
            ),
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )


    answer=response.choices[
        0
    ].message.content


    await chat_collection.insert_one(

        {

            "query":question,
            "answer":answer,
            "createdAt":datetime.utcnow()

        }

    )



    return answer