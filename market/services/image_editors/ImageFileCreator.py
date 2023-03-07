from copy import copy
from datetime import datetime
from os import mkdir, path, stat
from shutil import copyfileobj

from PIL.ImageFile import ImageFile
from fastapi import Depends, HTTPException, UploadFile
from PIL import Image

from .ImageFileEditor import ImageFileEditor


class ImageFileCreator(ImageFileEditor):

    @staticmethod
    def is_validate_file(image: ImageFile, content_type: str) -> bool:
        validators = [
            content_type == 'image/jpeg',
            image.size < (1920, 1280),
            len(image.fp.read()) < 3000000,
        ]
        return True if all(validators) else False

    @staticmethod
    async def _create_url(folder_name: str) -> str:
        return f'{folder_name}/{datetime.utcnow()}.jpg'.replace(':', '-')

    async def __call__(self, temp_file: UploadFile, folder_name: str) -> str:
        image, content_type = Image.open(temp_file.file), temp_file.content_type
        if self.is_validate_file(image, content_type):
            url = await self._create_url(folder_name)
            if not path.exists(f'{self.root_url}{folder_name}'):
                mkdir(f'{self.root_url}{folder_name}')
            image.save(f'{self.root_url}{url}')
        else:
            raise HTTPException(422, detail='Image file is not correct')
        return url
