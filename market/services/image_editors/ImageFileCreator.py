from datetime import datetime
from os import mkdir, path

from PIL.ImageFile import ImageFile
from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

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
        try:
            image, content_type = Image.open(temp_file.file), temp_file.content_type
            if self.is_validate_file(image, content_type):
                url = await self._create_url(folder_name)
                if not path.exists(f'{self.root_url}{folder_name}'):
                    mkdir(f'{self.root_url}{folder_name}')
                image.save(f'{self.root_url}{url}')
            else:
                raise UnidentifiedImageError
            return url
        except UnidentifiedImageError:
            raise HTTPException(422, 'The image file is incorrect')