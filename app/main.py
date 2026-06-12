from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
)

from app.models.api import SplitBillRequest

from app.services.bill_processor import BillProcessor
from app.services.image_receipt_processor import (
    ImageReceiptProcessor,
)


app = FastAPI()

processor = BillProcessor()

image_processor = ImageReceiptProcessor()


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


@app.post("/extract-receipt-image")
async def extract_receipt_image(
    file: UploadFile = File(...)
):

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp",
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format",
        )

    image_bytes = await file.read()

    receipt = image_processor.process(
        image_bytes=image_bytes,
        mime_type=file.content_type,
    )

    return receipt.model_dump()