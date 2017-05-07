#!/usr/bin/env python3

# example2.py
# SENG3011 - Cool Bananas
#
# An example query for the second API that should get converted

from datetime import datetime, date
from seng.core.constants import DB_DATE_FORMAT
import urllib.request
import json, sys

stingray_url = 'http://ec2-54-160-211-66.compute-1.amazonaws.com:3000/api/company_returns?'

class CompanyReturn(object):

    def __init__(self, data):
        super(CompanyReturn, self).__init__()

        # TODO: Asserts.

        self._ric = data['InstrumentID']
        self._data = []
        for d in data['Data']:
            self._data.append(Data(d))

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
        if 'CM_Return' in data:
            self._cm_return = data['CM_Return']
        else:
            self._cm_return = None
        if 'AV_Return' in data:
            self._av_return = data['AV_Return']
        else:
            self._av_return = None
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
    s = 'InstrumentID='
    for r in rics:
        s += r
        s += ','
    s = s[:-1]
    return s

# Converts the submitted vars into the format required for the SPARQL.
def get_var_filter(var):
    s = ''
    for v in var:
        s += 'ListOfVar='
        s += v
        s += '&'
    s = s[:-1]
    return s


# Converts the submitted date into the format required for the SPARQL.
def get_date_filter(d):
    s = 'DateOfInterest='
    s += str(d.day)
    s += '%2F'
    s += str(d.month)
    s += '%2F'
    s += str(d.year)
    return s

def result_date_convert(s):
    return date(int(s[0:4]), int(s[5:7]), int(s[8:10]))

# Does the query.
def do_query(query):
    print(query)
    return urllib.request.urlopen(query).read().decode('utf-8')

# Converts the arguments into the proper SPARQL command, then does it.
def query(rics=[], var=[], upper_window=0, lower_window=0, date_of_interest=date(1970, 1, 1)):
    r = get_ric_filter(rics)
    v = get_var_filter(var)
    u = 'UpperWindow=' + str(upper_window)
    l = 'LowerWindow=' + str(lower_window)
    d = get_date_filter(date_of_interest)
    return do_query(stingray_url + r + '&' + v + '&' + u + '&' + l + '&' + d)

# Turns the json.loads object data into proper classes.
def generate_company_returns(data):
    # TODO: Asserts.
    company_returns = []
    for c in data['CompanyReturns']:
        company_returns.append(CompanyReturn(c))

    return company_returns

def run():
    results = query(
        rics = ('ABP.AX',),
        var = ('AV_Return', 'CM_Return'),
        upper_window = 5,
        lower_window = 3,
        date_of_interest = date(2012, 12, 10)
    )

    data = json.loads(results)

    print(json.dumps(data, indent=4, separators=(',', ': ')))

    company_returns = generate_company_returns(data)

    pass

if __name__ == '__main__':
    run()
