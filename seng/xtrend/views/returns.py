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

    def get(self, request, ric):
        query = companyreturn.stingrayQuery((ric,), ('AV_Return', 'CM_Return'), 14, 90, date(2015, 12, 31))
        returnCSV = 'date,close\n'
        for r in query:
            if r.ric == ric:
                for d in r.data:
                    returnCSV += '{},{}\n'.format(d.date, d.adjusted_close)
        return HttpResponse(returnCSV, content_type='text/csv')

