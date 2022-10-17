from datetime import datetime
from os import path, mkdir, remove
from shutil import copyfileobj

from fastapi import UploadFile, HTTPException


class ImageFileUploader:

    @staticmethod
    def _is_validate_file(image_file: UploadFile) -> bool:
        if image_file.content_type == 'image/jpeg':
            return True
        else:
            return False

    def __init__(self, temp_file: UploadFile, folder_name: str) -> None:
        if self._is_validate_file(temp_file):
            self._temp_file: UploadFile = temp_file
            self._folder_name: str = folder_name
        else:
            raise HTTPException(422, detail='Image file is not correct')

    async def _create_url(self) -> str:
        return f'{self._folder_name}/{datetime.utcnow()}.jpg'.replace(':', '-')

    async def upload(self) -> str:
        url = await self._create_url()
        if not path.exists(f'media/{self._folder_name}'):
            mkdir(f'media/{self._folder_name}')
        with open(f'media/{url}', 'wb') as file:
            copyfileobj(self._temp_file.file, file)
        return url


class ImageFileDeleter:

    @staticmethod
    async def check_image_exist(url: str) -> bool:
        return path.exists(url)

    def __init__(self, prefix: str, url: str) -> None:
        self._url = path.join(prefix, url)

    async def delete(self) -> None:
        if await self.check_image_exist(self._url):
            remove(self._url)
        else:
            raise HTTPException(
                500,
                detail=f'Image file is not exist. Url: ({self._url})'
            )
