from datetime import datetime
from os import mkdir, path, stat
from shutil import copyfileobj

from fastapi import Depends, HTTPException, UploadFile
from PIL import Image

from .ImageFileEditor import ImageFileEditor


class ImageFileCreator(ImageFileEditor):

    @staticmethod
    def is_validate_file(image_file: UploadFile) -> bool:
        validators = [
            image_file.content_type == 'image/jpeg',
            Image.open(image_file.file).size < (1920, 1280),
            stat(image_file.file.fileno()).st_size < 3000000,
        ]
        return True if all(validators) else False

    @staticmethod
    async def _create_url(folder_name: str) -> str:
        return f'{folder_name}/{datetime.utcnow()}.jpg'.replace(':', '-')

    async def __call__(self, temp_file: UploadFile, folder_name: str) -> str:
        if self.is_validate_file(temp_file):
            url = await self._create_url(folder_name)
            if not path.exists(f'{self.root_url}{folder_name}'):
                mkdir(f'{self.root_url}{folder_name}')
            with open(f'{self.root_url}{url}', 'wb') as file:
                copyfileobj(temp_file.file, file)
        else:
            raise HTTPException(422, detail='Image file is not correct')
        return url
