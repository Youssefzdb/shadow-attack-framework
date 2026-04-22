import logging
import sys

def setup_logger(verbose=False):
    logger = logging.getLogger("shadow-attack")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("\033[90m%(asctime)s\033[0m %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
