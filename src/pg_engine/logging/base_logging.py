from __future__ import annotations

import logging

from .constants import LOG_FORMATTER_FORMATS, LOG_TIME_FORMAT

_logger = logging.getLogger('pg_engine')


class BaseFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # noqa: PLR6301
        log_fmt = LOG_FORMATTER_FORMATS.get(record.levelno)
        formatter = logging.Formatter(
            log_fmt,
            datefmt=LOG_TIME_FORMAT,
        )
        return formatter.format(record)

    @classmethod
    def apply(
        cls,
        logger: logging.Logger,
        level: logging._Level = logging.DEBUG,
    ) -> None:
        """
        Apply this formatter onto a logger.

        :param logger: logger to apply this formatter on
        :type logger: logging.Logger
        :param level: loglevel to set the logger to, defaults to logging.DEBUG
        :type level: logging._Level, optional
        """
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(cls())
        logger.addHandler(handler)
        logger.setLevel(level)


def set_loglevel(level: logging._Level, logger: logging.Logger | None = None) -> None:
    """
    Set the loglevel of a logger, default to this library's logger.

    :param level: log level to set the logger to
    :type level: logging._Level
    :param logger: Logger to update or this library's logger, defaults to None
    :type logger: logging.Logger | None, optional
    """
    if logger is None:
        logger = _logger
    logger.setLevel(level)


BaseFormatter.apply(_logger, logging.DEBUG)
