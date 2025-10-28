import logging

LOG_NORMAL_FONT = '\x1b[20m'
LOG_BOLD = '\x1b[1m'
LOG_GREY = '\x1b[38m'
LOG_LIGHT_CYAN = '\x1b[96m'
LOG_YELLOW = '\x1b[33m'
LOG_RED = '\x1b[31m'
LOG_RESET = '\x1b[0m'

LOG_TIME_FORMAT = '%H:%M:%S'
LOG_FORMAT = (
    LOG_BOLD +
    '{color}'
    '%(levelname)s' + LOG_NORMAL_FONT + ' [%(name)s - %(asctime)s]: '
    + LOG_RESET
    + '%(message)s (%(filename)s:%(lineno)d)'
)

LOG_FORMATTER_FORMATS = {
    logging.DEBUG:    LOG_FORMAT.format(color=LOG_GREY),
    logging.INFO:     LOG_FORMAT.format(color=LOG_LIGHT_CYAN),
    logging.WARNING:  LOG_FORMAT.format(color=LOG_YELLOW),
    logging.ERROR:    LOG_FORMAT.format(color=LOG_RED),
    logging.CRITICAL: LOG_FORMAT.format(color=LOG_RED),
}

__all__ = [
    'LOG_BOLD',
    'LOG_FORMAT',
    'LOG_FORMATTER_FORMATS',
    'LOG_GREY',
    'LOG_LIGHT_CYAN',
    'LOG_NORMAL_FONT',
    'LOG_RED',
    'LOG_RESET',
    'LOG_TIME_FORMAT',
    'LOG_YELLOW',
]
