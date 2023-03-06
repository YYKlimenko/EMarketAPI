from abc import ABC

from fastapi import Depends

from market.configs import MediaConfig


class ImageFileEditor(ABC):

    def __init__(self, media_config: MediaConfig = Depends()):
        self.root_url = media_config.url
