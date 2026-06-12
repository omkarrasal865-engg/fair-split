import time

from starlette.middleware.base import (
    BaseHTTPMiddleware,
)

from app.utils.logger import (
    logger,
)


class RequestLoggingMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next,
    ):

        start_time = time.time()

        request_id = getattr(
            request.state,
            "request_id",
            "unknown",
        )

        logger.info(
            f"[{request_id}] "
            f"Started {request.method} "
            f"{request.url.path}"
        )

        response = await call_next(
            request
        )

        duration = round(
            time.time() - start_time,
            3,
        )

        logger.info(
            f"[{request_id}] "
            f"Completed {request.method} "
            f"{request.url.path} "
            f"status={response.status_code} "
            f"duration={duration}s"
        )

        return response