from django.db import models
from collections import OrderedDict

from ..core.constants import API_DATE_FORMAT

class NewsArticle(models.Model):

    uri = models.CharField(null = False, unique = True, max_length = 120)
    language = models.CharField(null = False, max_length = 5)
    time_stamp = models.DateTimeField(null = False)
    headline = models.CharField(null = False, max_length = 50)
    news_text = models.TextField(null = False)

    def to_json(self):
        rics = NewsArticleRIC.objects.filter(article = self.id).all()
        topics = NewsArticleTopicCode.objects.filter(article = self.id).all()

        json = OrderedDict()
        json['URI'] = self.uri
        json['Language'] = self.language
        json['TimeStamp'] = self.time_stamp.strftime(API_DATE_FORMAT)[:-4] + 'Z'
        json['Headline'] = self.headline
        json['NewsText'] = self.news_text
        json['InstrumentIDs'] = sorted(set(map(lambda r: r.ric, rics)))
        json['TopicCodes'] = sorted(set(map(lambda t: t.topic_code, topics)))
        return json

class NewsArticleRIC(models.Model):

    article = models.ForeignKey(NewsArticle)
    ric = models.CharField(null = False, max_length = 20)

    class Meta:
        unique_together = (('article', 'ric'),)

class NewsArticleTopicCode(models.Model):

    article = models.ForeignKey(NewsArticle)
    topic_code = models.CharField(null = False, max_length = 20)

    class Meta:
        unique_together = (('article', 'topic_code'),)
