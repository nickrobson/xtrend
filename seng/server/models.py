from django.db import models
from collections import OrderedDict

from ..core.constants import API_DATE_FORMAT

class NewsArticle(models.Model):

    uri = models.CharField(max_length = 120)
    language = models.CharField(max_length = 5)
    time_stamp = models.DateTimeField()
    headline = models.CharField(max_length = 30)
    news_text = models.TextField()
    instrument_ids = models.TextField()
    topic_codes = models.TextField()
    query_instrument_ids = models.TextField()
    query_topic_codes = models.TextField()

    def to_json(self):
        json = OrderedDict()
        json['URI'] = self.uri
        json['Language'] = self.language
        json['TimeStamp'] = self.time_stamp.strftime(API_DATE_FORMAT)[:-4] + 'Z'
        json['Headline'] = self.headline
        json['NewsText'] = self.news_text
        json['InstrumentIDs'] = sorted(set(self.instrument_ids.split(',')))
        json['TopicCodes'] = sorted(set(self.topic_codes.split(',')))
        return json
