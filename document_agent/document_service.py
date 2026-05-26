from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os

from database import document_collection

load_dotenv()

endpoint = os.getenv("ENDPOINT")
key = os.getenv("KEY")

client = DocumentIntelligenceClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)


def clean_value(value):

    if not value:
        return None

    text = value.strip()

    lines = text.split("\n")

    unique = []

    for line in lines:

        line = line.strip()

        if line and line not in unique:
            unique.append(line)

    return " ".join(unique)


def extract_invoice_data(file_path):

    with open(file_path, "rb") as f:

        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            body=f
        )

    result = poller.result()

    extracted = {}

    if result.documents:

        doc = result.documents[0]

        for name, field in doc.fields.items():

            extracted[name] = clean_value(
                field.content
            )

    save_data = {

        "invoice_id":
        extracted.get("InvoiceId"),

        "supplier":
        extracted.get("VendorName"),

        "amount":
        extracted.get("InvoiceTotal"),

        "date":
        extracted.get("InvoiceDate"),

        "address":
        extracted.get("VendorAddress")

    }

    document_collection.insert_one(
        save_data
    )

    return extracted