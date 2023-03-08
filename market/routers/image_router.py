"""The Image Model endpoints."""

__all__ = ['image_router']

from typing import Any

from fastapi import APIRouter, Depends, UploadFile

from common.permissions import permit_for_admin
from common.functions import get_fields
from market.schemas import RetrievingImageSchema
from market.services import ImageService
from market.services.image_editors import ImageFileManager

image_router = APIRouter(prefix='/images', tags=['Images'])


@image_router.get(
    '/',
    status_code=200,
    description='Get a list of images',
    response_model=list[RetrievingImageSchema],
)
async def get_images(product_id: int | None = None, service: ImageService = Depends()) -> list[dict[str, Any]]:
    return await service.retrieve(many=True, **get_fields(product_id=product_id))


@image_router.get(
    '/{image_id}/',
    status_code=200,
    description='Get the image',
    response_model=RetrievingImageSchema | None,
)
async def get_image(image_id: int, service: ImageService = Depends()) -> dict[str, Any]:
    return await service.retrieve(id=image_id)


@image_router.post(
    '/',
    status_code=201,
    description='Create the image',
    dependencies=[Depends(permit_for_admin)],
)
async def post_image(
        file: UploadFile,
        product_id: int,
        service: ImageService = Depends(),
        image_editor: ImageFileManager = Depends(),
) -> None:
    return await service.create_image(file, product_id, image_editor)


@image_router.delete(
    '/{image_id}/',
    status_code=202,
    description='Delete the image',
    dependencies=[Depends(permit_for_admin)],
)
async def delete_image(
        image_id: int,
        service: ImageService = Depends(),
        image_editor: ImageFileManager = Depends()
) -> None:
    return await service.delete_image(image_id, image_editor)
