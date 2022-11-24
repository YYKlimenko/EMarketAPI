from fastapi import APIRouter, Depends, UploadFile, Form, Path
from sqlalchemy.engine import Row

from market.objects import PERMIT_FOR_ADMIN
from market.services import ImageService
from market.utils.image_edit import ImageEditor

router = APIRouter(tags=['Images'])


@router.get(
    '/images/',
    status_code=200,
    description='Get a list of images',
)
async def get_images(product_id: int | None = None, service: ImageService = Depends()) -> list[Row]:
    return await service.retrieve_list(product_id=product_id)


@router.get(
    '/images/{id}/',
    status_code=200,
    description='Get the image',
)
async def get_image(_id: int = Path(alias='id'), service: ImageService = Depends()) -> Row:
    return await service.retrieve_by_id(_id)


@router.post(
    '/images/',
    status_code=201,
    description='Create the image',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def post_image(
        file: UploadFile,
        product_id: int = Form(),
        service: ImageService = Depends(),
        image_editor: ImageEditor = Depends()
) -> None:
    return await service.create_image(file, product_id, image_editor)


@router.delete(
    '/images/{id}/',
    status_code=202,
    description='Delete the image',
    dependencies=[PERMIT_FOR_ADMIN]
)
async def delete_image(
        _id: int = Path(alias='id'),
        service: ImageService = Depends(),
        image_editor: ImageEditor = Depends()
) -> None:
    return await service.delete_image(_id, image_editor)
