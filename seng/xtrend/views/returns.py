# returns.py
# SENG3011 - Cool Bananas
#
# Gets company returns for a specific Instrument ID

from django.template.loader import get_template
from django.http import HttpResponse

from ...utils import SingletonView

class ReturnsView(SingletonView):

    def __init__(self):
        with open('static/xtrend/data.csv') as f:
            self.data = f.read()

    def get(self, request):
        return HttpResponse(self.data, content_type='text/html')

