from fastapi import APIRouter, UploadFile, File
import shutil
import os

from document_agent.document_service import (
    extract_invoice_data
)

from database import document_collection

router = APIRouter()

UPLOAD_DIR="uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/document-agent/extract")
async def extract_document(
    file: UploadFile=File(...)
):

    file_path=f"{UPLOAD_DIR}/{file.filename}"

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    data=extract_invoice_data(
        file_path
    )

    save_data={

        "invoice_id":
        data.get("InvoiceId"),

        "supplier":
        data.get("VendorName"),

        "amount":
        data.get("InvoiceTotal"),

        "date":
        data.get("InvoiceDate"),

        "address":
        data.get("VendorAddress")

    }

    document_collection.insert_one(
        save_data
    )

    return {

        "status":"success",

        "data":data
    }


@router.get("/document-agent/history")
async def history():

    docs = await document_collection.find(
        {},
        {"_id":0}
    ).to_list(length=100)

    return {

        "count": len(docs),

        "history": docs

    }