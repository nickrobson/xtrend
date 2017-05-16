# article.py
# SENG3011 - Cool Bananas
#
# Gets an article by a URI

import html

from django.template.loader import get_template
from django.http import HttpResponse, Http404

from .. import models
from ...utils import SingletonView
from ...core.constants import URI_PATTERN

def format_body(text):
    lines = text.split('\n    ')
    lines = map(lambda line: '<p>%s</p>' % line, lines)
    return '\n\n'.join(lines)

def get_polarity_image(polarity):
    if polarity > .1:
        return '/coolbananas/static/sentiment/arrow_up.svg'
    if polarity < -.1:
        return '/coolbananas/static/sentiment/arrow_down.svg'
    return '/coolbananas/static/sentiment/neutral.svg'

class APIArticleView(SingletonView):

    def __init__(self):
        self.template = get_template('assets/api/article.html')

    def get(self, request, uri = None):
        if uri is None:
            raise Http404('You need to specify an article URI!')
        if not URI_PATTERN.fullmatch(uri):
            raise Http404('Invalid URI!')
        article = models.NewsArticle.objects.get(uri = uri)
        if article is None:
            raise Http404('There is no article with URI: %s' % (uri,))
        render_context = {
            'article': {
                'headline': article.headline,
                'timestamp': article.time_stamp,
                'body': format_body(article.news_text),
                'uri': article.uri,
                'polarity': article.polarity,
                'polarity_image': get_polarity_image(article.polarity),
            },
        }
        content = self.template.render(render_context)
        return HttpResponse(content, content_type='text/html')
