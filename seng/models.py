from django.db import models

class NewsArticle(models.Model):
    uri = models.CharField(max_length = 120)
    time_stamp = models.DateTimeField()
    headline = models.CharField(max_length = 30)
    news_text = models.TextField()
    instrument_ids = models.TextField()
    topic_codes = models.TextField()
    query_instrument_ids = models.TextField()
    query_topic_codes = models.TextField()