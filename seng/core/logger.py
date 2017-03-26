# logger.py
# SENG3011 - Cool Bananas
#
# Handles logging messages

import logging

_LOGGING_LEVEL = logging.DEBUG

logger = logging.getLogger('SENG3011')
logger.setLevel(_LOGGING_LEVEL)

formatter = logging.Formatter('%(asctime)s - %(levelname)s\n   %(message)s', '%Y-%m-%d %H:%M:%S')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler('access.log', encoding='utf-8')
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def _tostring(*message):
    return ' '.join(map(str, message))

def debug(*message):
    logger.debug(_tostring(*message))

def info(*message):
    logger.info(_tostring(*message))

def warn(*message):
    logger.warn(_tostring(*message))

def error(*message):
    logger.error(_tostring(*message))

def critical(*message):
    logger.critical(_tostring(*message))

def exception(*message):
    logger.exception(*message)
