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

class RatingsView(SingletonView):

    def __init__(self):
        self.rics = sparql.get_rics()

    def get(self, request):

        s = 'RIC,Rating\n'
        for ric in self.rics:
            print('Doing ' + ric)
            s += ric + ',' + str(get_rating(ric)) + '\n'
        
        return HttpResponse(s, content_type='text/plain')

