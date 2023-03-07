"""Repositories types to the market application."""

__all__ = ['CategoryService', 'ImageService', 'ProductService', 'OrderService', 'UserService']

import os
import shutil
from http.client import HTTPException
from typing import Any

from fastapi import Depends, UploadFile

from common.services import AbstractService
from market.configs import MediaConfig
from market.repositories import (CategorySQLRepository, UserSQLRepository, ImageSQLRepository, ProductSQLRepository,
                                 OrderSQLRepository)
from market.services.image_editors import ImageFileManager


class CategoryService(AbstractService):
    """Category model's service class."""

    def __init__(self, repository: CategorySQLRepository = Depends()):
        """Init a service instance."""
        super().__init__(repository=repository)


class UserService(AbstractService):
    """User model's service class."""

    def __init__(self, repository: UserSQLRepository = Depends()):
        """Init a service instance."""
        super().__init__(repository=repository)


class ProductService(AbstractService):
    """User model's service class."""

    def __init__(self, repository: ProductSQLRepository = Depends(), media_config: MediaConfig = Depends()):
        """Init a service instance."""
        self.media_config = media_config
        super().__init__(repository=repository)

    async def delete(self, instance_id: int) -> None:
        await super().delete(instance_id=instance_id)
        shutil.rmtree(os.path.join(self.media_config.url, str(instance_id)), ignore_errors=True)


class ImageService(AbstractService):
    """Image model's service class."""

    def __init__(self, repository: ImageSQLRepository = Depends()):
        """Init a service instance."""
        super().__init__(repository=repository)

    async def create_image(
            self, file: UploadFile, product_id: int, image_manager: ImageFileManager
    ) -> None:
        """Create image file and call base create method."""
        url = await image_manager.create(file, str(product_id))
        try:
            await self.create({'url': url, 'product_id': product_id})
        except HTTPException:
            await image_manager.delete(url)
            raise

    async def delete_image(self, image_id: int, image_manager: ImageFileManager) -> None:
        """Delete image file and call base delete method."""
        if image := await self.retrieve(id=image_id):
            await self.delete(image_id)
            await image_manager.delete(image['url'])


class OrderService(AbstractService):
    """Order model's service class."""

    def __init__(self, repository: OrderSQLRepository = Depends()):
        """Init a service instance."""
        super().__init__(repository=repository)
