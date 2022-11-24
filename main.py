import logging

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from auth.router import router as auth_router
from loggs.config import LOGGING_CONFIG
from market.routers import category, product, image, user, order
from middlewares import handle_unknown_exception

app = FastAPI()
for router in (
        auth_router, category.router, product.router,
        image.router, user.router,  order.router
):
    app.include_router(router)


@app.on_event("startup")
async def startup_event():
    logging.config.dictConfig(LOGGING_CONFIG)

app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=handle_unknown_exception)
