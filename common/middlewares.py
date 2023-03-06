"""Middleware functions."""

import logging
import traceback
from typing import Callable, Any

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


async def handle_undefined_exception(
        request: Request, call_next: Callable[..., Any]
) -> JSONResponse:
    """Handle undefined exceptions."""
    try:
        response = await call_next(request)
        return response
    except Exception as exception:
        logger.error("uncaught exception: %s", traceback.format_exc())
        return JSONResponse(status_code=500, content={'exception': str(exception)})
