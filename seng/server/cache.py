# cache.py
# SENG3011 - Cool Bananas
#
# Caches queries so we don't use the database too much.

import operator

from collections import OrderedDict
from functools import reduce
from django.db.models import Q

from .models import NewsArticle, NewsArticleRIC, NewsArticleTopicCode
from ..core import logger, sparql, result as dbresult

cache = {}

def query(rics=[], topics=[], date_range=[]):
    logger.debug('Searching in LOCAL database')

    db_query = reduce(operator.and_, (
        Q(time_stamp__gte = date_range[0]),
        Q(time_stamp__lte = date_range[1])
    ))

    if len(rics):
        db_query &= Q(newsarticleric__ric__in = rics)

    if len(topics):
        db_query &= Q(newsarticletopiccode__topic_code__in = topics)

    key = (*sorted(rics), *sorted(topics), date_range[0], date_range[1])

    if key in cache:
        logger.debug('Query already in cache, getting results from cache')
        results = cache[key]
        return list(map(NewsArticle.to_json, results))

    results = NewsArticle.objects.filter(db_query).distinct()
    if len(results) > 0:
        logger.debug('Found query in LOCAL database and caching results')
        cache[key] = results
        return list(map(NewsArticle.to_json, results))

    results = sparql.query(
        rics = rics,
        topics = topics,
        date_range = date_range
    )

    json_result = results.to_json()

    for result in json_result:
        n, created = NewsArticle.objects.get_or_create(
            uri = result['URI'],
            defaults = {
                'language': result['Language'],
                'time_stamp': result['TimeStamp'],
                'headline': result['Headline'],
                'news_text': result['NewsText']
            })
        if created:
            n.save()

        for ric in result['InstrumentIDs']:
            r, created = NewsArticleRIC.objects.get_or_create(article = n, ric = ric)
            if created:
                r.save()

        for topic_code in result['TopicCodes']:
            t, created = NewsArticleTopicCode.objects.get_or_create(article = n, topic_code = topic_code)
            if created:
                t.save()

    logger.debug('Saved query to cache')

    return json_result
