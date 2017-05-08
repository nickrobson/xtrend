from django.db import models
from collections import OrderedDict

from ..core import logger
from ..core.constants import API_DATE_FORMAT
from ..core.sentiment import get_sentiment

class NewsArticle(models.Model):

    uri = models.CharField(null = False, unique = True, max_length = 120)
    language = models.CharField(null = False, max_length = 5)
    time_stamp = models.DateTimeField(null = False)
    headline = models.CharField(null = False, max_length = 50)
    news_text = models.TextField(null = False)
    polarity = models.FloatField()
    subjectivity = models.FloatField()

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
        json['Sentiment'] = OrderedDict([
            ('Polarity', self.polarity),
            ('Subjectivity', self.subjectivity)
        ])
        return json

    @classmethod
    def from_db(cls, db, field_names, values):
        inst = super().from_db(db, field_names, values)
        if inst.polarity < -1 or inst.polarity > 1 or inst.subjectivity < 0 or inst.subjectivity > 1:
            logger.info('No sentiment data found for article in LOCAL database - analysing.')
            sentiment = get_sentiment(inst.news_text)
            inst.polarity = sentiment.polarity
            inst.subjectivity = sentiment.subjectivity
            inst.save()
        return inst

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

class Company(models.Model):

    ric = models.CharField(null = False, unique = True, max_length = 20)
    name = models.CharField(null = False, max_length = 120)

    def to_json(self):
        return OrderedDict([
            ('InstrumentID', self.ric),
            ('Name', self.name),
        ])

class StockExchange(models.Model):

    code = models.CharField(null = False, unique = True, max_length = 5)
    name = models.CharField(null = False, unique = True, max_length = 120)

    def to_json(self):
        return OrderedDict([
            ('Code', self.code),
            ('Name', self.name),
        ])
