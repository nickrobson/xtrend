# analysis.py
# SENG3011 - Cool Bananas
#
# Displays stock analysis for a particular RIC

import math

from django.template.loader import get_template
from django.http import HttpResponse, Http404

from ...core import mk
from ...core.constants import RIC_PATTERN
from ...server.models import NewsArticle
from ...utils import SingletonView

def format_body(text):
    lines = text.split('\n    ')[:6]
    lines = map(lambda line: '<p>%s</p>' % line, lines)
    return '\n\n'.join(lines)

def get_polarity_image(polarity):
    if polarity > .1:
        return '/coolbananas/static/xtrend/arrow_up.svg'
    if polarity < -.1:
        return '/coolbananas/static/xtrend/arrow_down.svg'
    return '/coolbananas/static/xtrend/neutral.svg'

class RICAnalysisView(SingletonView):

    def __init__(self):
        self.template = get_template('assets/xtrend/analysis.html')

    def get(self, request, ric = None):
        if ric is None:
            raise Http404('You need to specify an instrument ID!')
        if not RIC_PATTERN.fullmatch(ric):
            raise Http404('Invalid instrument ID!')
        articles = NewsArticle.objects.filter(newsarticleric__ric = ric).order_by('time_stamp').reverse()[:10].all()
        if not len(articles):
            raise Http404('We have no analysis on %s, as there are no news articles.' % ric)
        articles = list(map(lambda article: {
                'headline': article.headline,
                'timestamp': article.time_stamp.strftime('%H:%M%p, %b %d, %Y'),
                'body': format_body(article.news_text),
                'uri': article.uri,
                'polarity': article.polarity,
                'polarity_image': get_polarity_image(article.polarity),
                'polarity_width': 100 if -.1 < article.polarity < .1 else math.ceil(math.log(500+1.1**abs(article.polarity * 100))*10),
            }, articles))
        content = self.template.render({
            'InstrumentID': ric,
            'ArticlesFirst': articles[::2],
            'ArticlesSecond': articles[1::2],
        })
        return HttpResponse(content, content_type='text/html')

