from fastapi import Request
from fastapi.responses import (
    JSONResponse,
)
from fastapi.exceptions import (
    RequestValidationError,
)

from app.exceptions import (
    FairSplitException,
)


class ErrorHandlerMiddleware:

    @staticmethod
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "request_id": getattr(
                    request.state,
                    "request_id",
                    None,
                ),
                "error": "Invalid request",
                "details": exc.errors(),
            },
        )

    @staticmethod
    async def handle_custom_error(
        request: Request,
        exc: FairSplitException,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "request_id": getattr(
                    request.state,
                    "request_id",
                    None,
                ),
                "error": str(exc),
            },
        )

    @staticmethod
    async def handle_generic_error(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "request_id": getattr(
                    request.state,
                    "request_id",
                    None,
                ),
                "error": "Internal server error",
            },
        )