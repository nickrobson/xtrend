# result.py
# SENG3011 - Cool Bananas
#
# Defines the QueryResult object, which turns the master databases's responses into a Python object.
# This object has useful functions.

from datetime import datetime
import json

from .constants import API_DATE_FORMAT

class QueryResult(object):
    
    def __init__(self, data):
        super(QueryResult, self).__init__()

        assert data['s']['type'] == 'uri'
        assert data['ric']['type'] == 'literal'
        assert data['topicCode']['type'] == 'literal'
        assert data['headline']['type'] == 'literal'
        assert data['newsBody']['type'] == 'literal'
        assert data['time']['type'] == 'literal'
        assert data['time']['datatype'] == 'http://www.w3.org/2001/XMLSchema#dateTime'

        self._data = data
        self._uri = data['s']['value']
        self._ric = data['ric']['value']
        self._ric = self._ric[self._ric.find('_')+1:]
        self._topic_code = data['topicCode']['value']
        self._time = datetime.strptime(data['time']['value'][:-1] + '000Z', API_DATE_FORMAT)
        self._headline = data['headline']['value']
        self._news_body = data['newsBody']['value']

    @property
    def uri(self):
        return self._uri

    @property
    def ric(self):
        return self._ric

    @property
    def topic_code(self):
        return self._topic_code

    @property
    def time(self):
        return self._time

    @property
    def headline(self):
        return self._headline

    @property
    def news_body(self):
        return self._news_body

    def to_json(self):
        curr_result = {}
        curr_result["InstrumentID"] = self.ric
        curr_result['TimeStamp'] = self.time.strftime(API_DATE_FORMAT)[:-4] + 'Z'
        curr_result["Headline"] = self.headline
        curr_result["NewsText"] = self.news_body
        return curr_result

    def __str__(self):
        return '%s (%s)' % (self.headline, self.time.strftime('%c').replace('  ', ' '))

    def __hash__(self):
        return hash(self.uri)

    def __eq__(self, other):
        return self.uri == other.uri and \
            self.ric == other.ric and \
            self.topic_code == other.topic_code and \
            self.time == other.time and \
            self.headline == other.headline and \
            self.news_body == other.news_body

def to_json(results):
    json_result = {}
    json_result["NewsDataSet"] = list(map(QueryResult.to_json, results))
    return json_result