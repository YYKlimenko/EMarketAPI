from os import path, remove

from fastapi import HTTPException

from .ImageFileEditor import ImageFileEditor


class ImageFileDeleter(ImageFileEditor):

    @staticmethod
    async def is_image_exist(url: str) -> bool:
        return path.exists(url)

    async def __call__(self, url: str) -> None:
        url = path.join(self.root_url, url)
        if await self.is_image_exist(url):
            remove(url)
        else:
            raise HTTPException(500, detail=f'Image file is not exist. Url: ({url})')
