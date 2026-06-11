from pydantic import BaseModel


class SplitBillRequest(BaseModel):
    receipt_text: str
    description: str