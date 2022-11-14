from fastapi import APIRouter, Depends

from core.permissions.permissions import permit_for_admin
from market.schemas import Image
from market.objects import image_service as service


router = APIRouter(tags=['Images'])


@router.get(
    '/images/',
    status_code=200,
    description='Get a list of images',
)
async def get_images(response: list[Image] = Depends(service.retrieve_list)):
    return response


@router.get(
    '/images/{id}',
    status_code=200,
    description='Get the image',
)
async def get_image(response: Image = Depends(service.retrieve_by_id)):
    return response


@router.post(
    '/images/',
    status_code=202,
    description='Create the image',
    dependencies=[Depends(permit_for_admin)]
)
async def post_image(response: None = Depends(service.create_image)):
    return response


@router.delete(
    '/images/{id}',
    status_code=202,
    description='Delete the image',
    dependencies=[Depends(permit_for_admin)]
)
async def delete_image(response: None = Depends(service.delete_image)):
    return response
