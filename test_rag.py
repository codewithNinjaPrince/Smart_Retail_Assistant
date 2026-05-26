from rag.retriever import search_docs

results=search_docs(
    "high profit electronics in winter"
)

for item in results:
    print(item)