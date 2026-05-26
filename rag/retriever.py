from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

client = SearchClient(
    endpoint=os.getenv("SEARCH_ENDPOINT"),
    index_name=os.getenv("INDEX_NAME"),
    credential=AzureKeyCredential(
        os.getenv("SEARCH_KEY")
    )
)

def search_docs(query):

    results = client.search(
        search_text=query,
        top=5
    )

    docs=[]

    for item in results:
        docs.append(item["chunk"])

    return docs