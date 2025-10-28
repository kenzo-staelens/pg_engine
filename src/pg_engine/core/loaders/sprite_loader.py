import logging

import pygame

from pg_engine.core.bases import TSpriteConfig
from pg_engine.core.loaders.spritesheet import SpriteSheet, TColorkey

from .yaml_loader import YamlLoader

logger = logging.getLogger(__name__)


class SpriteLoader(YamlLoader):

    """Specialized loader for loading spritesheets from a yaml configuration."""

    def __init__(self, colorkey: TColorkey = None, **kw):
        """
        Initialize the loader.

        :param colorkey: Default colorkey for spritesheets, defaults to None
        :type colorkey: TColorkey, optional
        """
        super().__init__(**kw)
        self.colorkey = colorkey

    @classmethod
    def validate_sheet_keys(cls, name: str, sheet_data: TSpriteConfig) -> bool:
        """
        Check if a spritesheet configuration has all required keys filled in.

        :param name: name of the spritesheet configuration being loaded
        :type name: str
        :param sheet_data: data in the spritesheet configuration
        :type sheet_data: dict
        :return: whether the data is valid.
        :rtype: bool
        """
        valid = True
        for key in ('filename', 'width', 'height', 'rect', 'bindings'):
            if key not in sheet_data:
                logger.error("Spritesheet[%s]: key '%s' not found", name, key)
                valid = False
                continue
            if sheet_data[key] is None:
                logger.error("Spritesheet[%s]: key '%s' cannot be empty", name, key)
                valid = False
        return valid

    def load_sheet(self, sheet_data: TSpriteConfig) -> list[pygame.Surface]:
        """
        Load a single spritesheet's content.

        :param sheet_data: configuration data of the spritesheet
        :type sheet_data: dict
        :return: list of loaded sprites
        :rtype: list[pygame.Surface]
        """
        sheet = SpriteSheet(sheet_data['filename'], root=self.root)
        rect = sheet_data['rect']
        width = sheet_data['width']
        height = sheet_data['height']
        colorkey = sheet_data.get('colorkey', self.colorkey)
        sheet.set_colorkey(colorkey)
        return [
            sheet.image_at(
                [
                    rect[0] + rect[2] * col,
                    rect[1] + rect[3] * row,
                    rect[2],
                    rect[3],
                ],
            )
            for row in range(height)
            for col in range(width)
        ]

    def load(self) -> dict[str, pygame.Surface]:
        """
        Load and register all sprites from all spritesheets.

        null/None image names get discarded.

        :return: mapping of spritesheets as {name: sprite}
        :rtype: dict[str, pygame.Surface]
        """
        data: dict[str, TSpriteConfig] = super().load()
        loaded = {}
        for spritesheet, conf in data.items():
            if not self.validate_sheet_keys(spritesheet, conf):
                continue
            sprites = self.load_sheet(conf)
            for binding, sprite in zip(conf['bindings'], sprites, strict=True):
                if not binding:
                    continue
                if binding in loaded:
                    logger.error(
                        "While loading sprite another entry '%s' was already found",
                        binding,
                    )
                    continue
                self.register_loaded(binding, sprite)
                loaded[binding] = sprite
        return loaded
