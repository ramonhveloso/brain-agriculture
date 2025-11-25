import time

from fastapi import Request

from app.core.log import get_logger

log = get_logger("api")


async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    log.info(
        "request_received",
        method=request.method,
        path=request.url.path,
        client=request.client.host,
    )

    response = await call_next(request)

    duration = round((time.time() - start_time) * 1000, 2)

    log.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=duration,
    )

    return response
