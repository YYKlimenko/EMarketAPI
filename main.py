import logging

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from auth.configs import AuthConfig, AuthConfigDev
from auth.router import router as auth_router  # type: ignore
# from common.middlewares import handle_unknown_exception
from loggs.config import LOGGING_CONFIG
from market.configs import PostgresConfig, PostgresConfigDev
from market.routers import category_router, user_router, image_router, product_router, order_router

app = FastAPI(debug=True)
for router in (auth_router, category_router, image_router, user_router, product_router, order_router):
    app.include_router(router)


@app.on_event("startup")
async def startup_event():
    if app.debug:
        app.dependency_overrides[PostgresConfig] = PostgresConfigDev
        app.dependency_overrides[AuthConfig] = AuthConfigDev
    # logging.config.dictConfig(LOGGING_CONFIG)

# app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=handle_unknown_exception)
