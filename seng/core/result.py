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
        assert data['id']['type'] == 'literal'
        assert data['ric']['type'] in ('literal', 'uri')
        assert data['topicCode']['type'] == 'literal'
        assert data['lang']['type'] == 'literal'
        assert data['headline']['type'] == 'literal'
        assert data['newsBody']['type'] == 'literal'
        assert data['time']['type'] == 'literal'
        assert data['time']['datatype'] in ('http://www.w3.org/2001/XMLSchema#dateTime', 'http://www.w3.org/2001/XMLSchema#dateTimeStamp')

        self._data = data
        self._uri = data['id']['value']
        self._ric = data['ric']['value']
        self._ric = self._ric[self._ric.find('_')+1:]
        self._topic_code = data['topicCode']['value'][3:]
        self._language = data['lang']['value']
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
    def language(self):
        '''
        This article's language
        '''
        return self._language

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
            self.language == other.language and \
            self.time == other.time and \
            self.headline == other.headline and \
            self.news_body == other.news_body


class QueryResultSet(object):

    '''
    Represents a set of articles from the database.
    '''

    def __init__(self, results):
        super(QueryResultSet, self).__init__()

        print(len(results))

        # This is a set that turns all the results through the function QueryResult (in this case it's the constructor).
        # It is not a hash map, it's just a set.
        self.results = set(map(QueryResult, results))
        self.results = sorted(self.results, key=lambda r: r.uri) # sort by uri
        self.json_results = []

        for uri, group in groupby(self.results, lambda r: r.uri): # group by uri
            items = list(group)
            if not len(items):
                continue
            first = items[0]

            out = OrderedDict()
            out['URI'] = uri
            out['Language'] = first.language
            out['TimeStamp'] = first.time.strftime(API_DATE_FORMAT)[:-4] + 'Z'
            out['Headline'] = first.headline
            out['NewsText'] = first.news_body
            out['InstrumentIDs'] = sorted(set(reduce(lambda a, b: a + [ b.ric ], items, [])))
            out['TopicCodes'] = sorted(set(reduce(lambda a, b: a + [ b.topic_code ], items, [])))

            self.json_results.append(out)

    def __iter__(self):
        return iter(self.results)

    def to_json(self):
        '''
        Turns this query result set to a JSON-compatible object
        '''
        return OrderedDict([('NewsDataSet', self.json_results)])
