# result.py
# SENG3011 - Cool Bananas
#
# Defines the QueryResult object, which turns the master database's responses into a Python object.

import json

from collections import OrderedDict
from datetime import datetime

from .constants import API_DATE_FORMAT

class QueryResult(object):

    '''
    Represents a single article from the database.
    '''
    
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

    def to_json(self):
        '''
        Turns this article into a dictionary serializable into JSON.
        '''
        curr_result = OrderedDict()
        #curr_result["URI"] = self.uri
        curr_result["InstrumentID"] = self.ric
        #curr_result["TopicCode"] = self.topic_code
        curr_result['TimeStamp'] = self.time.strftime(API_DATE_FORMAT)[:-4] + 'Z'
        curr_result["Headline"] = self.headline
        curr_result["NewsText"] = self.news_body
        return curr_result

    def __hash__(self):
        return hash(self.uri)

    def __eq__(self, other):
        return self.uri == other.uri and \
            self.ric == other.ric and \
            self.topic_code == other.topic_code and \
            self.time == other.time and \
            self.headline == other.headline and \
            self.news_body == other.news_body

class hashabledict(dict):
  def __key(self):
    return tuple((k, self[k]) for k in sorted(self))
  def __hash__(self):
    return hash(self.__key())
  def __eq__(self, other):
    return self.__key() == other.__key()

class hashablelist(list):
    def __hash__(self):
        return hash(tuple(self))
    def __eq__(self, other):
        return self == other

def uniq_list(the_list):
    the_set = set(map(lambda d: hashabledict(d), the_list))
    return list(map(lambda d: OrderedDict(d), the_set))

def to_json(results, uniq=False):
    '''
    Turns multiple QueryResult objects into an array of them, as a JSON serializable array.
    '''

    results_dict = {}
    for result in results:
        existing = results_dict.get(result.uri)
        if existing is not None:
            existing['TopicCodes'].add(result.topic_code)
            existing['InstrumentIDs'].add(result.ric)
        else:
            jr = result.to_json()
            existing = {}
            existing['URI'] = result.uri
            ric = jr.pop('InstrumentID')
            existing.update(jr)
            existing['InstrumentIDs'] = set([ ric ])
            existing['TopicCodes'] = set([ result.topic_code ])
        results_dict[result.uri] = existing

    all_results = []

    for k, v in results_dict.items():
        v = OrderedDict(v)
        v['TopicCodes'] = hashablelist(sorted(v['TopicCodes']))
        v['InstrumentIDs'] = hashablelist(sorted(v['InstrumentIDs']))
        all_results.append(v)

    if uniq:
        all_results = uniq_list(all_results)

    json_result = {}
    json_result["NewsDataSet"] = all_results
    return json_result
