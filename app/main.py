from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    Request,
)

from app.models.clarification_answer import (
    ClarificationRequest,
)

from app.services.clarification_service import (
    ClarificationService,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from fastapi.exceptions import (
    RequestValidationError,
)

from app.models.api import (
    SplitBillRequest,
    ApiSuccessResponse,
)

from app.models.clarification_answer import (
    ClarificationRequest,
)

from app.services.bill_processor import (
    BillProcessor,
)

from app.services.image_receipt_processor import (
    ImageReceiptProcessor,
)

from app.services.image_bill_processor import (
    ImageBillProcessor,
)

from app.services.clarification_service import (
    ClarificationService,
)

from app.middleware.error_handler import (
    ErrorHandlerMiddleware,
)

from app.middleware.request_id import (
    RequestIdMiddleware,
)

from app.middleware.request_logging import (
    RequestLoggingMiddleware,
)

from app.exceptions import (
    FairSplitException,
)

from app.validators.file_validator import (
    FileValidator,
)


app = FastAPI()

# -------------------------------
# CORS
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Custom Middleware
# -------------------------------

app.add_middleware(
    RequestIdMiddleware
)

app.add_middleware(
    RequestLoggingMiddleware
)

# -------------------------------
# Exception Handlers
# -------------------------------

app.add_exception_handler(
    RequestValidationError,
    ErrorHandlerMiddleware.handle_validation_error,
)

app.add_exception_handler(
    FairSplitException,
    ErrorHandlerMiddleware.handle_custom_error,
)

app.add_exception_handler(
    Exception,
    ErrorHandlerMiddleware.handle_generic_error,
)

# -------------------------------
# Services
# -------------------------------

processor = BillProcessor()

image_processor = (
    ImageReceiptProcessor()
)

image_bill_processor = (
    ImageBillProcessor()
)

clarification_service = (
    ClarificationService()
)

# -------------------------------
# Routes
# -------------------------------

@app.get("/")
def health_check(
    request: Request,
):
    return ApiSuccessResponse(
        request_id=request.state.request_id,
        data={
            "status": "healthy",
            "project": "FairSplit AI",
        },
    ).model_dump()


@app.post("/split-bill")
def split_bill(
    request_data: SplitBillRequest,
    request: Request,
):
    response = processor.process(
        receipt_text=request_data.receipt_text,
        description=request_data.description,
    )

    return ApiSuccessResponse(
        request_id=request.state.request_id,
        data=response.model_dump(),
    ).model_dump()


@app.post("/extract-receipt-image")
async def extract_receipt_image(
    request: Request,
    file: UploadFile = File(...),
):

    image_bytes = await file.read()

    FileValidator.validate(
        file_type=file.content_type,
        file_size=len(image_bytes),
    )

    receipt = image_processor.process(
        image_bytes=image_bytes,
        mime_type=file.content_type,
    )

    return ApiSuccessResponse(
        request_id=request.state.request_id,
        data=receipt.model_dump(),
    ).model_dump()


@app.post("/split-bill-image")
async def split_bill_image(
    request: Request,
    file: UploadFile = File(...),
    description: str = Form(...),
):

    image_bytes = await file.read()

    FileValidator.validate(
        file_type=file.content_type,
        file_size=len(image_bytes),
    )

    response = image_bill_processor.process(
        image_bytes=image_bytes,
        mime_type=file.content_type,
        description=description,
    )

    return ApiSuccessResponse(
        request_id=request.state.request_id,
        data=response.model_dump(),
    ).model_dump()


@app.post("/submit-clarification")
def submit_clarification(
    clarification_request: ClarificationRequest,
    request: Request,
):

    response = (
        clarification_service.process(
            clarification_request
        )
    )

    return ApiSuccessResponse(
        request_id=request.state.request_id,
        data=response.model_dump(),
    ).model_dump()

@app.post(
    "/clarification/{session_id}"
)
def submit_clarification(
    session_id: str,
    request_data: ClarificationRequest,
    request: Request,
):

    response = (
        clarification_service.process(
            session_id=session_id,
            clarification_request=request_data,
        )
    )

    return ApiSuccessResponse(
        request_id=request.state.request_id,
        data=response.model_dump(),
    ).model_dump()