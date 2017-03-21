# cache.py
# SENG3011 - Cool Bananas
#
# Caches queries so we don't use the database too much.

from seng import logger, sparql
from django.db.models import Q
from functools import reduce
from .models import NewsArticle

import operator
import seng.result

def query(rics=[], topics=[], date_range=[], uniq=False):

    db_query = Q(time_stamp__gte = date_range[0]) & Q(time_stamp__lte = date_range[1])

    if len(rics) > 0:
        db_query &= reduce(
            operator.or_, (
                Q(instrument_ids__contains = r) for r in rics
            )
        )

    if len(topics) > 0:
        db_query &= reduce(
            operator.or_, (
                Q(topic_codes__contains = t) for t in topics
            )
        )

    results = NewsArticle.objects.filter(db_query).all()
    if len(results) > 0:
        logger.debug('Found query in cache')
        return seng.result.from_db(results)

    results = sparql.query(
        rics = rics,
        topics = topics,
        date_range = date_range
    )

    json_result = seng.result.to_json(results, uniq = uniq)

    for result in json_result['NewsDataSet']:
        n = NewsArticle(
                uri = result['URI'],
                time_stamp = result['TimeStamp'],
                headline = result['Headline'],
                news_text = result['NewsText'],
                instrument_ids = ','.join(result['InstrumentIDs']),
                topic_codes = ','.join(result['TopicCodes'])
            )
        n.save() # Inserts into the database.

    logger.debug('Saved query to cache')

    return json_result