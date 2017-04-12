"""seng server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect

from .views import api, changelog, download, explorer, doc, homepage

admin.site.site_url = '/coolbananas/'

urlpatterns = [
    url(r'^coolbananas/admin/', admin.site.urls),
    url(r'^coolbananas/download/([0-9]+\.[0-9]+\.[0-9]+)/$', download.DownloadTagView.as_view()),
    url(r'^coolbananas/download/$', download.NoTagSpecifiedView.as_view()),
    url(r'^coolbananas/changelog/$', changelog.ChangeLogView.as_view()),
    url(r'^coolbananas/explorer/$', explorer.ExplorerView.as_view()),
    url(r'^coolbananas/documentation/$', doc.DocView.as_view()),
    url(r'^coolbananas/api/$', api.ApiView.as_view()),
    url(r'^coolbananas/$', homepage.HomepageView.as_view()),
    url(r'^$', lambda r: redirect('/coolbananas/')),
]
