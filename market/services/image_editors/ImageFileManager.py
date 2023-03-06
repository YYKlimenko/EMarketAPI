from fastapi import Depends

from market.services.image_editors import ImageFileCreator, ImageFileDeleter


class ImageFileManager:

    def __init__(
            self,
            creator: ImageFileCreator = Depends(),
            deleter: ImageFileDeleter = Depends()
    ) -> None:
        self.creator = creator
        self.deleter = deleter
