#!/usr/bin/env python3

# example2.py
# SENG3011 - Cool Bananas
#
# An example query for the second API that should get converted

from datetime import datetime, date
from seng.core.constants import DB_DATE_FORMAT
import urllib.parse
import urllib.request
import json, sys

stingray_url = 'http://ec2-54-160-211-66.compute-1.amazonaws.com:3000/api/company_returns?'

class CompanyReturn(object):

    def __init__(self, data):
        super(CompanyReturn, self).__init__()

        # TODO: Asserts.

        self._ric = data['InstrumentID']
        self._data = list(map(Data, data['Data']))

    @property
    def ric(self):
        '''
        This object's RIC or instrument ID.
        '''
        return self._ric

    @property
    def data(self):
        '''
        The array of all of this object's data.
        '''
        return self._data
    
class Data(object):
    def __init__(self, data):
        super(Data, self).__init__()
        
        # TODO: Asserts.

        self._relative_date = data['RelativeDate']
        self._date = result_date_convert(data['Date'])
        self._return = data['Return']
        self._return_percentage = data['Return_Percentage']
        self._cm_return = data.get('CM_Return')
        self._av_return = data.get('AV_Return')
        self._open = data['Open']
        self._high = data['High']
        self._low = data['Low']
        self._close = data['Close']
        self._adjusted_close = data['AdjustedClose']
        self._volume = data['Volume']

    @property
    def relative_date(self):
        '''
        This item's relative date.
        '''
        return self._relative_date
    
    @property
    def date(self):
        '''
        This item's date.
        '''
        return self._date
    
    @property
    def ret(self):
        '''
        This item's return.
        '''
        return self._ret
    
    @property
    def return_percentage(self):
        '''
        This item's return percentage.
        '''
        return self._return_percentage
    
    @property
    def cm_return(self):
        '''
        This item's CM_Return.
        '''
        return self._cm_return
    
    @property
    def av_return(self):
        '''
        This item's AV_Return.
        '''
        return self._av_return
    
    @property
    def open(self):
        '''
        This item's open.
        '''
        return self._open
    
    @property
    def high(self):
        '''
        This item's high.
        '''
        return self._high
    
    @property
    def low(self):
        '''
        This item's low.
        '''
        return self._low
    
    @property
    def close(self):
        '''
        This item's close.
        '''
        return self._close
    
    @property
    def adjusted_close(self):
        '''
        This item's adjusted close.
        '''
        return self._adjusted_close
    
    @property
    def volume(self):
        '''
        This item's volume.
        '''
        return self._volume

# Converts the submitted RIC string into the format required for the SPARQL.
def get_ric_filter(rics):
    return 'InstrumentID=' + ','.join(map(urllib.parse.quote, rics)) if len(rics) else ''

# Converts the submitted vars into the format required for the SPARQL.
def get_var_filter(var):
    return '&'.join(map(lambda s: 'ListOfVar=' + urllib.parse.quote(s), var))

# Converts the submitted date into the format required for the SPARQL.
def get_date_filter(d):
    return 'DateOfInterest=' + urllib.parse.quote(d.strftime('%d/%m/%Y'))

def result_date_convert(s):
    return date(*map(int, s.split('-')))

# Does the query.
def do_query(query):
    print(query)
    with urllib.request.urlopen(query) as conn:
        data = conn.read().decode()
    return data

# Converts the arguments into the proper SPARQL command, then does it.
def query(rics=[], var=[], upper_window=0, lower_window=0, date_of_interest=date(1970, 1, 1)):
    ric_filter = get_ric_filter(rics)
    var_filter = get_var_filter(var)
    date_filter = get_date_filter(date_of_interest)
    upper_window = 'UpperWindow={}'.format(upper_window)
    lower_window = 'LowerWindow={}'.format(lower_window)
    filters = [ric_filter, var_filter, upper_window, lower_window, date_filter]
    json_data = do_query(f'{stingray_url}{"&".join(filters)}')
    return json.loads(json_data)

# Turns the json.loads object data into proper classes.
def generate_company_returns(data):
    return list(map(CompanyReturn, data['CompanyReturns']))

def run():
    results = query(
        rics = ('ABP.AX',),
        var = ('AV_Return', 'CM_Return'),
        upper_window = 5,
        lower_window = 3,
        date_of_interest = date(2012, 12, 10)
    )

    print(json.dumps(results, indent=4, separators=(',', ': ')))

    company_returns = generate_company_returns(results)

    print(company_returns)

if __name__ == '__main__':
    run()
