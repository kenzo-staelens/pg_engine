from __future__ import annotations

import logging
from collections.abc import Callable

from pg_engine.api import (
    IGame,
    IProcessor,
    IRenderer,
    IUIManager,
)
from pg_engine.core import (
    TDisplayConfig,
    TRendererConfig,
    TUIManagerConfig,
)

logger = logging.getLogger(__name__)


class GraphicsProcessor(IProcessor):

    """
    Specialized processor to configure graphics components.

    :class:`IUIManager` and :class:`IRenderer`.
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
            processor_meth: Callable[[IGame, dict], None] = getattr(cls, meth)
            processor_meth(conf)

    @classmethod
    def _configure_renderer(cls, renderer_config: TRendererConfig) -> None:
        """Apply configurations as defined in :class:`TRendererConfig` onto a :class:`IRenderer` instance."""  # noqa: E501
        IRenderer().configure(renderer_config)

    @classmethod
    def _configure_uimanager(cls, ui_config: TUIManagerConfig) -> None:
        """Apply configurations as defined in :class:`TUIManagerConfig` onto a :class:`IUIManager` instance."""  # noqa: E501
        IUIManager().configure(ui_config)
