from datetime import datetime
from os import path, mkdir, remove
from shutil import copyfileobj

from fastapi import UploadFile, HTTPException, Depends

from market.configs.MediaConfig import MediaConfig


class ImageEditor:

    def __init__(self, media_config: MediaConfig = Depends()) -> None:
        self.root_url = media_config.url

    @staticmethod
    def is_validate_file(image_file: UploadFile) -> bool:
        if image_file.content_type == 'image/jpeg':
            return True
        else:
            return False

    @staticmethod
    async def _create_url(folder_name) -> str:
        return f'{folder_name}/{datetime.utcnow()}.jpg'.replace(':', '-')

    @staticmethod
    async def check_image_exist(url: str) -> bool:
        return path.exists(url)

    async def upload(self, temp_file: UploadFile, folder_name: str) -> str:
        if ImageEditor.is_validate_file(temp_file):
            temp_file: UploadFile = temp_file
            folder_name: str = folder_name
        else:
            raise HTTPException(422, detail='Image file is not correct')

        url = await self._create_url(folder_name)
        if not path.exists(f'{self.root_url}{folder_name}'):
            mkdir(f'{self.root_url}{folder_name}')
        with open(f'{self.root_url}{url}', 'wb') as file:
            copyfileobj(temp_file.file, file)
        return url

    async def delete(self, url: str) -> None:
        url = path.join(self.root_url, url)
        if await ImageEditor.check_image_exist(url):
            remove(url)
        else:
            raise HTTPException(500, detail=f'Image file is not exist. Url: ({url})')
