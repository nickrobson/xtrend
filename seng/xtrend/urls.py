from django.conf.urls import include, url
from django.http import HttpResponseNotFound
from django.template.loader import get_template
from django.urls.exceptions import Resolver404

from .views import article, analysis, homepage, ratings, returns, search, searchresults
from ..core.constants import RIC_PATTERN, RIC_LIST_PATTERN, URI_PATTERN

xtrend_urls = [
    url(r'^analysis/(?P<ric>'+RIC_PATTERN.pattern+')?$', analysis.RICAnalysisView.as_view()),
    url(r'^article/(?P<uri>'+URI_PATTERN.pattern+')?$', article.XtrendArticleView.as_view()),
    url(r'^returns/(?P<rics>'+RIC_LIST_PATTERN.pattern+')$', returns.ReturnsView.as_view()),
    url(r'^ratings/$', ratings.RatingsView.as_view()),
    url(r'^search/results/$', searchresults.SearchResultsView.as_view()),
    url(r'^search/$', search.SearchView.as_view()),
    url(r'^$', homepage.HomepageView.as_view()),
]

template404 = get_template('assets/xtrend/404.html')

def xtrend404(request, *args, **kwargs):
    exception = kwargs.get('exception')
    exceptionmsg = str(exception) if exception else 'Not Found'
    if isinstance(exception, Resolver404):
        exceptionmsg = 'Invalid URL!'
    content = template404.render({
        'exception': exceptionmsg,
        'path': request.path,
    })
    return HttpResponseNotFound(content, content_type='text/html')