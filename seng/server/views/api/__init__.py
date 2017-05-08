from django.conf.urls import url

from .base import ApiView
from .rics import RicsView
from .topics import TopicsView
from .dates import DatesView
from .companies import CompaniesView

urls = [
    url('^$', ApiView.as_view()),
    url('^rics/$', RicsView.as_view()),
    url('^topics/$', TopicsView.as_view()),
    url('^dates/$', DatesView.as_view()),
    url('^companies/(?P<ric>[A-Z0-9]+)/$', CompaniesView.as_view()),
    url('^companies/$', CompaniesView.as_view()),
]