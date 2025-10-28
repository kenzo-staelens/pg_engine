from __future__ import annotations

import logging
import pathlib
import sys

import pygame

from pg_engine.core.exit_codes import ExitCodes

type TColorkey = pygame.Color | tuple[int, int, int] | None

logger = logging.getLogger(__name__)


class SpriteSheet:
    def __init__(self, filename: str, root: pathlib.PosixPath):
        """
        Initialize a SpriteSheet wrapper around an image file.

        :param filename: file to wrap.
        :type filename: str
        :param root: path to search files in
        :type root: pathlib.PosixPath
        :raises SystemExit: raised when pygame cannot load the
        """
        try:
            self.sheet = pygame.image.load(root / filename).convert_alpha()
        except pygame.error:
            logger.exception('Unable to load spritesheet image: %s', filename)
            sys.exit(ExitCodes.EXIT_CODE_LOAD_SPRITESHEET)
        self.colorkey = None

    # Load a specific image from a specific rectangle
    def image_at(
        self,
        rectangle: pygame.Rect | tuple[int, int, int, int],
        ) -> pygame.Surface:
        """
        Get image data from this spritesheet at `rectangle`.

        :param rectangle: x,y, width, heigth of the image to get
        :type rectangle: pygame.Rect | tuple[int, int, int, int]
        :return: the image data at rectangle as a surface with :func:`convert_alpha`.
        :rtype: pygame.Surface
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if self.colorkey is not None:
            if self.colorkey == -1:
                self.colorkey = image.get_at((0, 0))
            image.set_colorkey(self.colorkey, pygame.RLEACCEL)
        return image.convert_alpha()

    @classmethod
    def rect_for(cls, rect_def: tuple[int, int, int, int]) -> pygame.Rect:
        """
        Convert a tuple to a :class:`pygame.Rect`.

        :param rect_def: integer representation of the rectangle
        :type rect_def: tuple[int, int, int, int]
        :return: a pygame rectangle
        :rtype: pygame.Rect
        """
        return pygame.Rect(rect_def)

    def set_colorkey(self, colorkey: TColorkey) -> None:
        """
        Set the :attr:`colorkey` of this spritesheet.

        .. note::
            used by :func:`pygame.Surface.set_colorkey`

        :param colorkey: _description_
        :type colorkey: TColorkey
        """
        if colorkey is None or colorkey == -1:
            self.colorkey = colorkey
            return
        if isinstance(colorkey, pygame.Color):
            self.colorkey = colorkey
            return
        self.colorkey = pygame.Color(colorkey)
