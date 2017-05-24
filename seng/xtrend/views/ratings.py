# ratings.py
# SENG3011 - Cool Bananas
#
# Gets all the ratings for each RIC.

import json

from collections import OrderedDict
from datetime import date
from django.template.loader import get_template
from django.http import HttpResponse

from ...utils import SingletonView

from ..core.rating import get_rating
from ...core import sparql

_CHECKED_RICS = sparql.get_rics()
_CHECKED_RICS = list(filter(lambda ric: ric.endswith('.AX'), _CHECKED_RICS))

def get_ratings(rics = None):
    if rics is None:
        rics = _CHECKED_RICS
    res = {}
    for ric in rics:
        res[ric] = get_rating(ric)
    return res

class RatingsView(SingletonView):

    def __init__(self):
        self.ratings = get_ratings()

    def get(self, request):
        return HttpResponse(json.dumps(self.ratings), content_type='application/json')
