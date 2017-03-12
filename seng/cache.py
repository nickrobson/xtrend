# cache.py
# SENG3011 - Cool Bananas
#
# Caches queries so we don't use the database too much.

import cachetools

from seng import logger, result, sparql

CACHE = cachetools.TTLCache(maxsize = 250, ttl = 600)

def query(rics=[], topics=[], date_range=[]):
    key = CacheKey(
        rics = rics,
        topics = topics,
        date_range = date_range
    )

    if key in CACHE:

        logger.debug('Found query in cache')

        return CACHE[key]

    results = sparql.query(
        rics = rics,
        topics = topics,
        date_range = date_range
    )
    json_result = result.to_json(results, uniq=True)

    CACHE[key] = json_result

    logger.debug('Saved query to cache')

    return json_result

class CacheKey(object):

    def __init__(self, rics=[], topics=[], date_range=[]):
        self._rics = rics
        self._topics = topics
        self._date_range = date_range
        self._key = (*self._rics, *self._topics, *self._date_range)

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        return self._key == other._key
