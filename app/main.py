from fastapi import FastAPI

from app.models.api import SplitBillRequest
from app.services.bill_processor import BillProcessor


app = FastAPI()

processor = BillProcessor()


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "project": "Fair Split"
    }


@app.post("/split-bill")
def split_bill(
    request: SplitBillRequest
):
    response = processor.process(
        receipt_text=request.receipt_text,
        description=request.description,
    )

    return response.model_dump()