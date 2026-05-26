import os
import sys
import types
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017")
os.environ.setdefault("DB_NAME", "smara_test")
os.environ.setdefault("AZURE_LANGUAGE_ENDPOINT", "https://example.cognitiveservices.azure.com/")
os.environ.setdefault("AZURE_LANGUAGE_KEY", "test-key")
os.environ.setdefault("ENDPOINT", "https://example.cognitiveservices.azure.com/")
os.environ.setdefault("KEY", "test-key")
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com/")
os.environ.setdefault("AZURE_OPENAI_KEY", "test-key")
os.environ.setdefault("CHAT_DEPLOYMENT", "test-deployment")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class FakeDemandModel:
    def predict(self, data):
        return [125.75]


class FakeAnomalyModel:
    def predict(self, data):
        return [1]


class FakeScaler:
    def transform(self, values):
        return values


class FakeSeries:
    def quantile(self, value):
        return 100 if value >= 0.75 else 50


class FakeDataFrame:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __getitem__(self, key):
        return FakeSeries()


class FakeAsyncCursor:
    def __init__(self, rows):
        self.rows = rows

    def sort(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def __aiter__(self):
        self._iter = iter(self.rows)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration as exc:
            raise StopAsyncIteration from exc

    async def to_list(self, length=None):
        return self.rows[:length]


class FakeCollection:
    def __init__(self, rows=None):
        self.rows = rows or []

    def find(self, *args, **kwargs):
        return FakeAsyncCursor(list(self.rows))

    async def insert_one(self, doc):
        doc.setdefault("_id", "test-id")
        self.rows.append(doc)
        return SimpleNamespace(inserted_id="test-id")


class FakeSyncCollection:
    def __init__(self, rows=None):
        self.rows = rows or []

    def find(self, *args, **kwargs):
        return FakeAsyncCursor(list(self.rows))

    def insert_one(self, doc):
        doc.setdefault("_id", "test-id")
        self.rows.append(doc)
        return SimpleNamespace(inserted_id="test-id")


def install_import_stubs():
    joblib_stub = types.ModuleType("joblib")
    joblib_stub.load = lambda path: FakeScaler() if "scaler" in path else FakeDemandModel()
    sys.modules.setdefault("joblib", joblib_stub)

    pandas_stub = types.ModuleType("pandas")
    pandas_stub.read_csv = lambda *args, **kwargs: FakeDataFrame()
    pandas_stub.DataFrame = FakeDataFrame
    sys.modules.setdefault("pandas", pandas_stub)

    database_stub = types.ModuleType("database")
    database_stub.chat_collection = FakeCollection()
    database_stub.document_collection = FakeSyncCollection()
    database_stub.retail_collection = FakeCollection()
    sys.modules.setdefault("database", database_stub)

    rag_chat_stub = types.ModuleType("rag.chat")

    async def fake_ask_rag(question):
        return "Mocked sales insight"

    rag_chat_stub.ask_rag = fake_ask_rag
    sys.modules.setdefault("rag.chat", rag_chat_stub)

    document_service_stub = types.ModuleType("document_agent.document_service")
    document_service_stub.extract_invoice_data = lambda path: {
        "InvoiceId": "INV-1",
        "VendorName": "Demo Vendor",
    }
    sys.modules.setdefault("document_agent.document_service", document_service_stub)

    crew_stub = types.ModuleType("crew.retail_crew")

    async def fake_run_retail_crew(total_sales, monthly_growth, top_category):
        return "Mocked retail analysis"

    crew_stub.run_retail_crew = fake_run_retail_crew
    sys.modules.setdefault("crew.retail_crew", crew_stub)

    bson_stub = types.ModuleType("bson")
    bson_stub.ObjectId = lambda value=None: value or "test-id"
    sys.modules.setdefault("bson", bson_stub)

    dotenv_stub = types.ModuleType("dotenv")
    dotenv_stub.load_dotenv = lambda *args, **kwargs: None
    sys.modules.setdefault("dotenv", dotenv_stub)

    azure_stub = types.ModuleType("azure")
    azure_core_stub = types.ModuleType("azure.core")
    azure_credentials_stub = types.ModuleType("azure.core.credentials")
    azure_credentials_stub.AzureKeyCredential = lambda key: SimpleNamespace(key=key)
    azure_ai_stub = types.ModuleType("azure.ai")
    azure_text_stub = types.ModuleType("azure.ai.textanalytics")

    class FakeTextAnalyticsClient:
        def __init__(self, *args, **kwargs):
            pass

        def analyze_sentiment(self, documents):
            return [
                SimpleNamespace(
                    sentiment="positive",
                    confidence_scores=SimpleNamespace(positive=0.98),
                )
            ]

    azure_text_stub.TextAnalyticsClient = FakeTextAnalyticsClient
    sys.modules.setdefault("azure", azure_stub)
    sys.modules.setdefault("azure.core", azure_core_stub)
    sys.modules.setdefault("azure.core.credentials", azure_credentials_stub)
    sys.modules.setdefault("azure.ai", azure_ai_stub)
    sys.modules.setdefault("azure.ai.textanalytics", azure_text_stub)


install_import_stubs()

from fastapi.testclient import TestClient

import api.anomaly_api as anomaly_api
import api.crew_routes as crew_routes
import api.demand_api as demand_api
import api.document_routes as document_routes
import api.rag_api as rag_api
import api.sentiment_routes as sentiment_routes
from main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]


def test_predict_demand(monkeypatch):
    monkeypatch.setattr(demand_api, "model", FakeDemandModel())
    monkeypatch.setattr(demand_api, "low_demand", 50)
    monkeypatch.setattr(demand_api, "high_demand", 100)

    payload = {
        "Price": 99.99,
        "Discount": 5.0,
        "Holiday": 0,
        "Season": 1,
        "Weather": 2,
        "Customer_Footfall": 250,
        "Marketing_Spend": 1000.0,
        "Competitor_Price": 95.0,
        "Inventory_Level": 500,
        "Year": 2026,
        "Month": 5,
        "Day": 25,
        "Weekday": 1,
        "Quarter": 2,
        "Profit_Margin": 0.25,
        "Inventory_Ratio": 0.75,
        "Marketing_Efficiency": 1.5,
    }

    response = client.post("/predict-demand", json=payload)

    assert response.status_code == 200
    assert response.json()["demand_level"] == "High"
    assert "predicted_units_sold" in response.json()


def test_predict_anomaly(monkeypatch):
    monkeypatch.setattr(anomaly_api, "model", FakeAnomalyModel())
    monkeypatch.setattr(anomaly_api, "scaler", FakeScaler())

    payload = {
        "Units_Sold": 80,
        "Price": 49.99,
        "Discount": 10.0,
        "Customer_Footfall": 200,
        "Marketing_Spend": 750.0,
        "Inventory_Level": 300,
        "Profit": 1200.0,
    }

    response = client.post("/predict-anomaly", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "Normal"


def test_rag_ask_endpoint(monkeypatch):
    async def fake_ask_rag(query):
        return "Mocked sales insight"

    monkeypatch.setattr(rag_api, "ask_rag", fake_ask_rag)

    response = client.post(
        "/data-analyst-and-query-agent/ask",
        json={"query": "Which products are trending?"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Mocked sales insight"


def test_rag_history_endpoint(monkeypatch):
    monkeypatch.setattr(
        rag_api,
        "chat_collection",
        FakeCollection([{"_id": "abc123", "query": "test", "answer": "ok"}]),
    )

    response = client.get("/data-analyst-and-query-agent/history")

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_document_extract_endpoint(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "uploads").mkdir()
    monkeypatch.setattr(
        document_routes,
        "extract_invoice_data",
        lambda file_path: {"InvoiceId": "INV-1", "VendorName": "Demo Vendor"},
    )
    monkeypatch.setattr(document_routes, "document_collection", FakeSyncCollection())

    response = client.post(
        "/document-agent/extract",
        files={"file": ("invoice.txt", b"sample invoice", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["InvoiceId"] == "INV-1"


def test_document_history_endpoint(monkeypatch):
    monkeypatch.setattr(
        document_routes,
        "document_collection",
        FakeSyncCollection([{"invoice_id": "INV-1", "supplier": "Demo Vendor"}]),
    )

    response = client.get("/document-agent/history")

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_sentiment_analyze_and_history(monkeypatch):
    class FakeSentimentClient:
        def analyze_sentiment(self, documents):
            return [
                SimpleNamespace(
                    sentiment="positive",
                    confidence_scores=SimpleNamespace(positive=0.98),
                )
            ]

    monkeypatch.setattr(sentiment_routes, "client", FakeSentimentClient())
    sentiment_routes.history.clear()

    response = client.post(
        "/sentiment-agent/analyze",
        json={"review": "The store experience was excellent."},
    )

    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"

    history_response = client.get("/sentiment-agent/history")

    assert history_response.status_code == 200
    assert len(history_response.json()) == 1


def test_crew_analyze_and_history(monkeypatch):
    async def fake_run_retail_crew(total_sales, monthly_growth, top_category):
        return "Mocked retail analysis"

    collection = FakeCollection([{"_id": "abc123", "total_sales": 1000.0}])
    monkeypatch.setattr(crew_routes, "run_retail_crew", fake_run_retail_crew)
    monkeypatch.setattr(crew_routes, "retail_collection", collection)

    response = client.post(
        "/crew/analyze",
        json={
            "total_sales": 50000.0,
            "monthly_growth": 12.5,
            "top_category": "Electronics",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["analysis"] == "Mocked retail analysis"

    history_response = client.get("/crew/history")

    assert history_response.status_code == 200
    assert len(history_response.json()) >= 1
