# homepage.py
# SENG3011 - Cool Bananas
#
# Displays homepage with list of revisions of code

from django.template.loader import get_template
from django.http import HttpResponse

from .ratings import get_ratings
from ...utils import SingletonView

def html_format(item):
    ric, rating = item
    return {
        'InstrumentID': ric,
        'Rating': '{0:+0.4f}'.format(rating),
        'BarPercent': (rating + 100) / 2,
    }

class HomepageView(SingletonView):

    def __init__(self):
        template = get_template('assets/xtrend/homepage.html')
        ratings = sorted(get_ratings().items(), key = lambda item: item[1])
        best_buys = list(map(html_format, reversed(ratings[-3:])))
        best_sells = list(map(html_format, ratings[:3]))
        self.content = template.render({
            'BestBuys': best_buys,
            'BestSells': best_sells,
        })

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')

