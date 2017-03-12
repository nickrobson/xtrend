# logger.py
# SENG3011 - Cool Bananas
#
# Handles logging messages

import logging

_LOGGING_LEVEL = logging.DEBUG

logger = logging.getLogger('SENG3011')
logger.setLevel(_LOGGING_LEVEL)

formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s\n   %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler('access.log', encoding='utf-8')
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def debug(message):
    logger.debug(message)

def info(message):
    logger.info(message)

def warn(message):
    logger.warn(message)

def error(message):
    logger.error(message)

def critical(message):
    logger.critical(message)
