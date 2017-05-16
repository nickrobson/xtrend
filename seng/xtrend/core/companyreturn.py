# companyreturn.py
# SENG3011 - Cool Bananas
#
# Stores the data for a company return.

from . import companydata
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
        self._data = list(map(companydata.CompanyData, data['Data']))

    @property
    def ric(self):
        '''
        This object's RIC or instrument ID.
        '''
        return self._ric

    @property
    def data(self):
        '''
        The array of all of this object's company data.
        '''
        return self._data

# Converts the arguments into the proper SPARQL command, does it, then converts it to an object.
def stingrayQuery(rics=[], var=[], upper_window=0, lower_window=0, date_of_interest=date(1970, 1, 1)):
    ric_filter = 'InstrumentID=' + ','.join(map(urllib.parse.quote, rics)) if len(rics) else ''
    var_filter = '&'.join(map(lambda s: 'ListOfVar=' + urllib.parse.quote(s), var))
    date_filter = 'DateOfInterest=' + urllib.parse.quote(date_of_interest.strftime('%d/%m/%Y'))
    upper_window = 'UpperWindow={}'.format(upper_window)
    lower_window = 'LowerWindow={}'.format(lower_window)
    filters = [ric_filter, var_filter, upper_window, lower_window, date_filter]
    data = None
    with urllib.request.urlopen(f'{stingray_url}{"&".join(filters)}') as conn:
        data = json.loads(conn.read().decode())
    return list(map(CompanyReturn, data['CompanyReturns']))