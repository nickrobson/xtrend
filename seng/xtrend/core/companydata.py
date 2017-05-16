# companydata.py
# SENG3011 - Cool Bananas
#
# Stores a single item for company data.

from datetime import datetime, date
from seng.core.constants import DB_DATE_FORMAT
import urllib.parse
import urllib.request
import json, sys

class CompanyData(object):
    def __init__(self, data):
        super(CompanyData, self).__init__()
        
        # TODO: Asserts.

        self._relative_date = data['RelativeDate']
        self._date = date(*map(int, data['Date'].split('-')))
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