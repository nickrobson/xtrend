from datetime import datetime

from .constants import API_DATE_FORMAT

class QueryResult(object):
    
    def __init__(self, data):
        super(QueryResult, self).__init__()
        self._data = data
        self._uri = data['s']['value']
        self._time = datetime.strptime(data['time']['value'][:-1] + '000Z', API_DATE_FORMAT)
        self._headline = data['headline']['value']
        self._news_body = data['newsBody']['value']

    @property
    def uri(self):
        return self._uri

    @property
    def time(self):
        return self._time

    @property
    def headline(self):
        return self._headline

    @property
    def news_body(self):
        return self._news_body

    def __str__(self):
        return self.headline

    def __hash__(self):
        return hash(self.uri)

    def __eq__(self, other):
        return self.uri == other.uri and \
            self.time == other.time and \
            self.headline == other.headline and \
            self.news_body == other.news_body
