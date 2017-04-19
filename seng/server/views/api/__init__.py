from django.conf.urls import url

from .base import ApiView
from .rics import RicsView
from .topics import TopicsView

urls = [
    url('^$', ApiView.as_view()),
    url('^rics/$', RicsView.as_view()),
    url('^topics/$', TopicsView.as_view())
]