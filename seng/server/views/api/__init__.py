from django.conf.urls import url

from .base import ApiView
from .rics import RicsView
from .topics import TopicsView
from .dates import DatesView
from .companies import CompaniesView

urls = [
    url(r'^$', ApiView.as_view()),
    url(r'^rics/$', RicsView.as_view()),
    url(r'^topics/$', TopicsView.as_view()),
    url(r'^dates/$', DatesView.as_view()),
    url(r'^companies/(?P<ric>[A-Z0-9]+)/$', CompaniesView.as_view()),
    url(r'^companies/$', CompaniesView.as_view()),
]