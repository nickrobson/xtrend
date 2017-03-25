# result.py
# SENG3011 - Cool Bananas
#
# Defines the QueryResult object, which turns the master database's responses into a Python object.

import json

from collections import OrderedDict
from datetime import datetime
from itertools import groupby
from functools import reduce

from .constants import API_DATE_FORMAT

class QueryResult(object):

    '''
    Represents a single article from the database.
    '''
    
    def __init__(self, data):
        super(QueryResult, self).__init__()

        assert data['s']['type'] == 'uri'
        assert data['ric']['type'] in ('literal', 'uri')
        assert data['topicCode']['type'] == 'literal'
        assert data['headline']['type'] == 'literal'
        assert data['newsBody']['type'] == 'literal'
        assert data['time']['type'] == 'literal'
        assert data['time']['datatype'] in ('http://www.w3.org/2001/XMLSchema#dateTime', 'http://www.w3.org/2001/XMLSchema#dateTimeStamp')

        self._data = data
        self._uri = data['s']['value']
        self._ric = data['ric']['value']
        self._ric = self._ric[self._ric.find('_')+1:]
        self._topic_code = data['topicCode']['value'][3:]
        self._time = datetime.strptime(data['time']['value'][:-1] + '000Z', API_DATE_FORMAT)
        self._headline = data['headline']['value']
        self._news_body = data['newsBody']['value']

    @property
    def uri(self):
        '''
        This article's URI.
        '''
        return self._uri

    @property
    def ric(self):
        '''
        This article's RIC, or instrument ID.
        '''
        return self._ric

    @property
    def topic_code(self):
        '''
        This article's topic code.
        '''
        return self._topic_code

    @property
    def time(self):
        '''
        This article's time stamp.
        '''
        return self._time

    @property
    def headline(self):
        '''
        This article's headline.
        '''
        return self._headline

    @property
    def news_body(self):
        '''
        This article's body text.
        '''
        return self._news_body

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
    '''
    Turns multiple QueryResult objects into an array of them, as a JSON serializable array.
    '''

    results = sorted(results, key=lambda r: r.uri) # sort first
    groups = groupby(results, lambda r: r.uri) # group by uri

    all_results = []

    for uri, group in groups:
        items = list(group)
        if not len(items):
            continue
        first = items[0]

        out = OrderedDict()
        out['URI'] = uri
        out['TimeStamp'] = first.time.strftime(API_DATE_FORMAT)[:-4] + 'Z'
        out['Headline'] = first.headline
        out['NewsText'] = first.news_body
        out['InstrumentIDs'] = sorted(set(reduce(lambda a, b: a + [ b.ric ], items, [])))
        out['TopicCodes'] = sorted(set(reduce(lambda a, b: a + [ b.topic_code ], items, [])))

        all_results.append(out)

    return OrderedDict([('NewsDataSet', all_results)])

def from_db(results):

    all_results = []

    for result in results:
        r = OrderedDict()
        r['URI'] = result.uri
        r['TimeStamp'] = result.time_stamp.strftime(API_DATE_FORMAT)[:-4] + 'Z'
        r['Headline'] = result.headline
        r['NewsText'] = result.news_text
        r['InstrumentIDs'] = sorted(set(result.instrument_ids.split(',')))
        r['TopicCodes'] = sorted(set(result.topic_codes.split(',')))
        all_results.append(r)

    return OrderedDict([('NewsDataSet', all_results)])
