import json
import urllib.parse
import urllib.request

from collections import OrderedDict
from datetime import date, timedelta
from django.db.models import Q
from django.db.utils import IntegrityError

from ..models import StockPrice

seesharp_url = 'http://174.138.67.207/'

def get(rics, upper_window, lower_window, doi):
    start_date, end_date = doi - timedelta(days = lower_window), doi + timedelta(days = upper_window)
    cache_hits = {}
    djq = Q(date__gte = start_date) & Q(date__lte = end_date)
    for ric in rics:
        prices = StockPrice.objects.filter(djq & Q(ric = ric)).distinct()
        if len(prices) == upper_window + lower_window + 1: # +1 to include doi
            cache_hits[ric] = list(prices)
    missing_rics = list(filter(lambda ric: ric not in cache_hits, rics))
    if len(missing_rics):
        query_results = []
        for ric in missing_rics:
            query_results.append(query_see_sharp(ric, upper_window, lower_window, doi))
        for result in query_results:
            cache_hits[result.ric] = result.data
            result.save()
    return cache_hits


def query_see_sharp(ric, upper_window, lower_window, doi):
    parameters = [
        ('InstrumentID', ric),
        ('DateOfInterest', doi.strftime('%Y-%m-%d')),
        ('List_of_Var', ','.join(['Minimum', 'Maximum', 'CM_Return', 'AV_Return', 'PC_Return', 'Trading_Info'])),
        ('Upper_window', upper_window),
        ('Lower_window', lower_window),
    ]
    parameters = map(lambda t: (t[0], str(t[1])), parameters)
    parameters = filter(lambda t: len(t[1]), parameters)
    parameters = map(lambda t: '{}/{}'.format(t[0], urllib.parse.quote(t[1])), parameters)
    query = '/'.join(parameters)
    url = seesharp_url + query
    try:
        with urllib.request.urlopen(url) as conn:
            data = json.loads(conn.read().decode())
        return SeeSharpCompanyReturn(data['CompanyReturns'][0])
    except:
        return SeeSharpCompanyReturn({'InstrumentID': ric})

class SeeSharpCompanyReturn(object):

    def __init__(self, data):
        super(SeeSharpCompanyReturn, self).__init__()

        self.ric = data['InstrumentID']
        self.minimum = SeeSharpMinimum(data.get('Minimum', {}))
        self.maximum = SeeSharpMaximum(data.get('Maximum', {}))
        self.data = list(map(SeeSharpCompanyData, data.get('Data', [])))

    def save(self):
        for datum in self.data:
            model = StockPrice(
                ric = self.ric,
                relative_date = datum.relative_date,
                date = datum.date,
                open = datum.open,
                high = datum.high,
                low = datum.low,
                close = datum.close,
                volume = datum.volume,
                adjusted_close = datum.adjusted_close,
                return_value = datum.return_value,
                pc_return = datum.pc_return,
                av_return = datum.av_return,
                cm_return = datum.cm_return
            )
            try:
                model.save()
            except IntegrityError as e:
                if not str(e).startswith('UNIQUE constraint failed'):
                    raise e

class SeeSharpCompanyData(object):

    def __init__(self, data):
        super(SeeSharpCompanyData, self).__init__()

        self.relative_date = data['RelativeDate']
        self.date = date(*map(int, data['Date'].split('-')))
        self.return_value = data['Return']
        self.pc_return = data['PC_Return']
        self.cm_return = data['CM_Return']
        self.av_return = data['AV_Return']

        trading_info = data['Trading_Info'] or {} # is null for a non-trading day
        self.open = trading_info.get('Open', -1)
        self.high = trading_info.get('High', -1)
        self.low = trading_info.get('Low', -1)
        self.close = trading_info.get('Close', -1)
        self.volume = trading_info.get('Volume', -1)
        self.adjusted_close = trading_info.get('AdjClose', -1)

    def to_dict(self):
        return OrderedDict([
            ('RelativeDate', self.relative_date),
            ('Date', self.date.strftime('%Y-%m-%d')),
            ('Return', self.return_value),
            ('Open', self.open),
            ('High', self.high),
            ('Close', self.close),
            ('Volume', self.volume),
            ('AdjustedClose', self.adjusted_close),
            ('PC_Return', self.pc_return),
            ('CM_Return', self.cm_return),
            ('AV_Return', self.av_return),
        ])

class SeeSharpMinimum(object):

    def __init__(self, data):
        super(SeeSharpMinimum, self).__init__()

class SeeSharpMaximum(object):

    def __init__(self, data):
        super(SeeSharpMaximum, self).__init__()
