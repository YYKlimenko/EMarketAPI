import logging

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from auth.router import router as auth_router
from common import setup
from common.middlewares import handle_unknown_exception
from loggs.config import LOGGING_CONFIG
from market.routers import category, image, order, product, user

app = FastAPI()
for router in (
        auth_router, category.router, product.router,
        image.router, user.router, order.router, setup.router
):
    app.include_router(router)


@app.on_event("startup")
async def startup_event():
    logging.config.dictConfig(LOGGING_CONFIG)

app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=handle_unknown_exception)
