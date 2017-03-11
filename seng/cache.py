# cache.py
# SENG3011 - Cool Bananas
#
# Caches queries so we don't use the database too much.

import cachetools

import seng.result
import seng.sparql

CACHE = cachetools.TTLCache(maxsize = 250, ttl = 600)

def query(rics=[], topics=[], date_range=[]):
    key = CacheKey(
        rics = rics,
        topics = topics,
        date_range = date_range
    )

    if key in CACHE:
        return CACHE[key]

    results = seng.sparql.query(
        rics = rics,
        topics = topics,
        date_range = date_range
    )
    result = seng.result.to_json(results)

    CACHE[key] = result

    return result

class CacheKey(object):

    def __init__(self, rics=[], topics=[], date_range=[]):
        self._rics = rics
        self._topics = topics
        self._date_range = date_range

    @property
    def _key(self):
        return (*self._rics, *self._topics, *self._date_range)

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        return self._key == other._key
