from . import logging
from . import core
from . import components
from . import systems
from . import base_scripts
from . import gui_extensions


def init() -> None:
    """Call :func:`pg_engine.core.bases.initializer.Initializer.init`."""
    core.Initializer.init()


def quit() -> None:  # noqa: A001
    """Call :func:`pg_engine.core.bases.initializer.Initializer.quit`."""
    core.Initializer.quit()
