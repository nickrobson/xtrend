# cache.py
# SENG3011 - Cool Bananas
#
# Caches queries so we don't use the database too much.

from seng import logger, result, sparql
from django.db import models

class NewsArticle(models.Model):
    instrument_id = models.CharField(max_length=30)
    time_stamp = models.CharField(max_length=30)
    headline = models.CharField(max_length=30)
    news_text = models.CharField(max_length=30)


def query(rics=[], topics=[], date_range=[], uniq=False):

    cache_values = NewsArticle.objects.filter(rics=rics).filter(topics=topics).filter(date_range=date_range).filter(uniq=uniq)


    if cache_values is not None:
        logger.debug('Found query in cache')
        return cache_val

    results = sparql.query(
        rics = rics,
        topics = topics,
        date_range = date_range
    )
    json_result = result.to_json(results, uniq=uniq)

    n = NewsArticle(
        instrument_id=json_result["InstrumentID"],
        time_stamp=json_result["TimeStamp"],
        headline=json_result["Headline"],
        news_text=json_result["NewsText"],
    )
    n.save() # Inserts into the database.

    logger.debug('Saved query to cache')

    return json_result