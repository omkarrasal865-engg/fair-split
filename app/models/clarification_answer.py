from pydantic import BaseModel


class ClarificationConsumer(BaseModel):
    person: str

    quantity: float


class ClarificationAnswer(BaseModel):
    question_id: str

    item: str

    consumers: list[
        ClarificationConsumer
    ]


class ClarificationRequest(BaseModel):
    answers: list[
        ClarificationAnswer
    ]