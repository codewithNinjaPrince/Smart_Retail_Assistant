import importlib

import rag.retriever as retriever_module


def test_search_docs_returns_empty_when_search_is_unconfigured(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.delenv("SEARCH_ENDPOINT", raising=False)
    monkeypatch.delenv("INDEX_NAME", raising=False)
    monkeypatch.delenv("SEARCH_KEY", raising=False)

    retriever_mod = importlib.reload(retriever_module)
    results = retriever_mod.search_docs("high profit electronics in winter")

    assert results == []