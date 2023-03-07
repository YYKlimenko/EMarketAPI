from fastapi import Depends, UploadFile

from market.services.image_editors import ImageFileCreator, ImageFileDeleter


class ImageFileManager:

    def __init__(
            self,
            creator: ImageFileCreator = Depends(),
            deleter: ImageFileDeleter = Depends()
    ) -> None:
        self.creator = creator
        self.deleter = deleter

    async def create(self, temp_file: UploadFile, folder_name: str):
        return await self.creator(temp_file, folder_name)

    async def delete(self, url: str):
        return await self.deleter(url)
