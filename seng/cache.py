# cache.py
# SENG3011 - Cool Bananas
#
# Caches queries so we don't use the database too much.

import cachetools

from seng import logger, result, sparql

CACHE = cachetools.TTLCache(maxsize = 250, ttl = 600)

def query(rics=[], topics=[], date_range=[], uniq=False):

    cache_key = (*rics, *topics, *date_range, uniq)
    cache_val = CACHE.get(cache_key)

    if cache_val is not None:
        logger.debug('Found query in cache')
        return cache_val

    results = sparql.query(
        rics = rics,
        topics = topics,
        date_range = date_range
    )
    json_result = result.to_json(results, uniq=uniq)

    CACHE[cache_key] = json_result

    logger.debug('Saved query to cache')

    return json_result
