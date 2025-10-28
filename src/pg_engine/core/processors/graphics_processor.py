from __future__ import annotations

import logging
from collections.abc import Callable

from pg_engine.core import (
    TDisplayConfig,
    TGame,
    TProcessor,
    TRenderer,
    TRendererConfig,
    TUIManager,
    TUImanagerConfig,
)

logger = logging.getLogger(__name__)


class GraphicsProcessor(TProcessor):

    """
    Specialized processor to configure graphics components.

    :class:`TUIManager` and :class:`TRenderer`.
    """

    @classmethod
    def process(
        cls,
        config: TDisplayConfig,
        processor_args: None = None,  # noqa: ARG003
    ) -> None:
        """
        Call configurationmethods `_configure_{x}` where x is a key in the configuration dict.

        :param config: display configuration dictionary
        :type config: TDisplayConfig
        :param processor_args: not used, defaults to None
        :type processor_args: None, optional
        """  # noqa: E501
        for key, conf in config.items():
            meth = f'_configure_{key}'
            if not hasattr(cls, meth):
                logger.warning(
                    "%s: Configuration method '%s' not found",
                    cls.__name__,
                    meth,
                )
                continue
            processor_meth: Callable[[TGame, dict], None] = getattr(cls, meth)
            processor_meth(conf)

    @classmethod
    def _configure_renderer(cls, renderer_config: TRendererConfig) -> None:
        """Apply configurations as defined in :class:`TRendererConfig` onto a :class:`TRenderer` instance."""  # noqa: E501
        TRenderer().configure(renderer_config)

    @classmethod
    def _configure_uimanager(cls, ui_config: TUImanagerConfig) -> None:
        """Apply configurations as defined in :class:`TUIManagerConfig` onto a :class:`TUIManager` instance."""  # noqa: E501
        TUIManager().configure(ui_config)
