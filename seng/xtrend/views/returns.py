# returns.py
# SENG3011 - Cool Bananas
#
# Gets company returns for a specific Instrument ID

from django.template.loader import get_template
from django.http import HttpResponse
from datetime import datetime, date

from ...utils import SingletonView
from ..core import companyreturn

class ReturnsView(SingletonView):

    def __init__(self):
        with open('static/xtrend/data.csv') as f:
            self.data = f.read()

    def get(self, request):
        query = companyreturn.stingrayQuery(('BHP.AX',), ('AV_Return', 'CM_Return'), 14, 90, date(2015, 12, 31))
        returnCSV = 'date,close\n'
        for r in query:
            if r.ric == 'BHP.AX':
                for d in r.data:
                    returnCSV += str(d.date) + ',' + str(d.adjusted_close) + '\n'
        return HttpResponse(returnCSV, content_type='text/plain')

