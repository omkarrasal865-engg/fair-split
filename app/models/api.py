from typing import Any

from pydantic import BaseModel


class SplitBillRequest(BaseModel):
    receipt_text: str
    description: str


class ApiSuccessResponse(BaseModel):
    success: bool = True

    request_id: str

    data: Any


class ApiErrorResponse(BaseModel):
    success: bool = False

    request_id: str | None = None

    error: str