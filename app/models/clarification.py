from pydantic import BaseModel


class ClarificationQuestion(BaseModel):
    id: str

    type: str

    item: str

    remaining_quantity: float

    remaining_amount: float

    question: str

    participants: list[str]


class ClarificationResponse(BaseModel):
    questions: list[
        ClarificationQuestion
    ]


class ClarificationAnswer(BaseModel):
    question_id: str

    allocations: dict[
        str,
        float,
    ]


class ClarificationSubmission(BaseModel):
    session_id: str

    answers: list[
        ClarificationAnswer
    ]