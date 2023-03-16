import logging
import sys


def my_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    format_color = {
        'grey': "\x1b[38;20m",
        'yellow': "\x1b[33;20m",
        'red': "\x1b[31;20m",
        'bold_red': "\x1b[31;1m",
        'reset': "\x1b[0m"
    }

    formatter = logging.Formatter(
        format_color['reset']+'%(levelname)s - %(asctime)s - %(name)s \n' + format_color['reset'] \
        + format_color['red']+'%(message)s' + format_color['red'])
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return (logger)
