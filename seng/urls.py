from django.conf.urls import include, url
from django.contrib import admin
from django.http import Http404
from django.shortcuts import redirect
from django.views.static import serve as static_serve

from .server.urls import api_urls, api404
from .xtrend.urls import xtrend_urls, xtrend404

admin.site.site_url = '/coolbananas/'

urlpatterns = [
    url(r'coolbananas/xtrend/', include(xtrend_urls)),
    url(r'coolbananas/static/(?P<path>.*)', static_serve, {'document_root': 'static'}),
    url(r'coolbananas/', include(api_urls)),
    url(r'^$', lambda r: redirect('/coolbananas/')),
]

def CB404(request, *args, **kwargs):
    path = request.path
    if path.startswith('/coolbananas/xtrend/'):
        return xtrend404(request, *args, **kwargs)
    return api404(request, *args, **kwargs)

handler404 = CB404