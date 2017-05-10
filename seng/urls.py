from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import redirect

from .server.urls import api_urls
from .xtrend.urls import xtrend_urls

admin.site.site_url = '/coolbananas/'

urlpatterns = [
    url(r'coolbananas/xtrend/', include(xtrend_urls)),
    url(r'coolbananas/', include(api_urls)),
    url(r'^$', lambda r: redirect('/coolbananas/')),
]
