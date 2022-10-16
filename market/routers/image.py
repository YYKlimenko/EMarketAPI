from fastapi import APIRouter, Depends

from auth.objects import authenticator
from core.settings import repository
from market.models import Image
from market.services import ImageService

router = APIRouter(tags=['Images'])
service = ImageService(repository)


@router.get('/images/')
async def get_images(response: list[Image] = Depends(service.retrieve_list)) -> list[Image]:
    return response


@router.get('/images/{id}')
async def get_image(response: Image = Depends(service.retrieve_by_id)) -> Image:
    return response


@router.post('/images/')
async def post_image(response: None = Depends(service.create_image)) -> None:
    return response


@router.delete('/images/{id}')
async def delete_image(response: None = Depends(service.delete_image)) -> None:
    return response
