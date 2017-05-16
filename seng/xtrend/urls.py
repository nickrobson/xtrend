from django.conf.urls import include, url

from .views import homepage, analysis, search, searchresults

xtrend_urls = [
    url(r'^analysis/$', analysis.RICAnalysisView.as_view()),
    url(r'^search/results/$', searchresults.SearchResultsView.as_view()),
    url(r'^search/$', search.SearchView.as_view()),
    url(r'^$', homepage.HomepageView.as_view()),
]