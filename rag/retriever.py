from dotenv import load_dotenv
import os

load_dotenv()

_client = None


def get_client():
    global _client

    if _client is not None:
        return _client

    endpoint = os.getenv("SEARCH_ENDPOINT")
    index_name = os.getenv("INDEX_NAME")
    key = os.getenv("SEARCH_KEY")

    if not all([endpoint, index_name, key]):
        return None

    try:
        from azure.search.documents import SearchClient
        from azure.core.credentials import AzureKeyCredential
    except ImportError:
        return None

    _client = SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(key),
    )

    return _client


def search_docs(query):
    client = get_client()

    if client is None:
        return []

    results = client.search(
        search_text=query,
        top=5,
    )

    docs = []

    for item in results:
        docs.append(item["chunk"])

    return docs