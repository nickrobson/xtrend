# returns.py
# SENG3011 - Cool Bananas
#
# Gets company returns for a specific Instrument ID

import json

from collections import OrderedDict
from datetime import date
from django.template.loader import get_template
from django.http import HttpResponse

from ..core import stocks
from ...utils import SingletonView

class ReturnsView(SingletonView):

    def get(self, request, rics):
        query = stocks.get(
            rics = rics.split(','),
            upper_window = 14,
            lower_window = 90,
            doi = date(2015, 12, 31)
        )
        response_json = OrderedDict()
        for ric, company_return in query.items():
            company_array = []
            for data in company_return:
                company_array.append(data.to_dict())
            response_json[ric] = company_array
        return HttpResponse(json.dumps(response_json), content_type='application/json')

