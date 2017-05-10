from django.conf.urls import include, url
from django.contrib import admin

from .views import api, changelog, download, explorer, doc, homepage

admin.site.site_url = '/coolbananas/'

api_urls = [
    url(r'^admin/', admin.site.urls),
    url(r'^download/([0-9]+\.[0-9]+\.[0-9]+)/$', download.DownloadTagView.as_view()),
    url(r'^download/$', download.NoTagSpecifiedView.as_view()),
    url(r'^changelog/$', changelog.ChangeLogView.as_view()),
    url(r'^explorer/$', explorer.ExplorerView.as_view()),
    url(r'^documentation/$', doc.DocView.as_view()),
    url(r'^api/', include(api.urls)),
    url(r'^$', homepage.HomepageView.as_view()),
]
