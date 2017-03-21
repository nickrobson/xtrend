from django.db import models

class NewsArticle(models.Model):
    uri = models.CharField(primary_key = True, max_length = 120)
    time_stamp = models.DateTimeField()
    headline = models.CharField(max_length = 30)
    news_text = models.TextField()
    instrument_ids = models.TextField()
    topic_codes = models.TextField()