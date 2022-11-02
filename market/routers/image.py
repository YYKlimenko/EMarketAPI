from fastapi import APIRouter, Depends

from auth.objects import authenticator
from core.repositories import SQLAsyncRepository, SQLAsyncRepository
from market.schemas import Image, CreatingImage
from market.services import ImageService
from market.models import ImageModel

router = APIRouter(tags=['Images'])
repository = SQLAsyncRepository(ImageModel)
service = ImageService(repository, Image, CreatingImage)


@router.get('/images/', status_code=200, description='Get a list of images')
async def get_images(response: list[Image] = Depends(service.retrieve_list)) -> list[Image]:
    return response


@router.get('/images/{id}', status_code=200, description='Get the image')
async def get_image(response: Image = Depends(service.retrieve_by_id)) -> Image:
    return response


@router.post('/images/', status_code=202, description='Create the image')
async def post_image(response: None = Depends(service.create_image)) -> None:
    return response


@router.delete('/images/{id}', status_code=202, description='Delete the image')
async def delete_image(response: None = Depends(service.delete_image)) -> None:
    return response
