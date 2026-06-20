from pydantic import BaseModel


class ClarificationQuestion(BaseModel):
    id: str

    type: str

    item: str

    remaining_quantity: float

    remaining_amount: float

    question: str


class ClarificationResponse(BaseModel):
    questions: list[
        ClarificationQuestion
    ]