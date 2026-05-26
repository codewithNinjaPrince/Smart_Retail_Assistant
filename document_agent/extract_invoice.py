from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os

load_dotenv()

endpoint = os.getenv("ENDPOINT")
key = os.getenv("KEY")

client = DocumentIntelligenceClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

pdf_path = os.path.join(
    BASE_DIR,
    "sample_docs",
    "invoices",
    "INV001.pdf"
)

with open(pdf_path, "rb") as f:

    poller = client.begin_analyze_document(
        "prebuilt-invoice",
        body=f
    )

result = poller.result()

print("\nEXTRACTED DATA\n")

for doc in result.documents:

    for name, field in doc.fields.items():

        print(
            f"{name}: {field.content}"
        )