from typing import Literal

from pydantic import BaseModel

from app.models.response import (
    FairSplitResponse,
)

from app.models.clarification import (
    ClarificationResponse,
)


class SplitResult(BaseModel):
    status: Literal[
        "completed",
        "needs_clarification",
    ]

    data: FairSplitResponse | None = None

    clarification: (
        ClarificationResponse | None
    ) = None

    session_id: str | None = None