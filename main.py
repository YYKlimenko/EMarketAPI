from fastapi import FastAPI
from auth.router import router as auth_router
from market.routers import category, product, image, user, order


app = FastAPI()
for router in (
        auth_router, category.router, product.router,
        image.router, user.router, order.router
):
    app.include_router(router)
