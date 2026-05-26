from rag.retriever import search_docs


def test_search_docs_returns_empty_when_search_is_unconfigured():
    results = search_docs("high profit electronics in winter")

    assert results == []