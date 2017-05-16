from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseNotFound
from django.template.loader import get_template
from django.urls.exceptions import Resolver404

from .views import api, article, changelog, download, explorer, doc, homepage
from ..core.constants import URI_PATTERN

admin.site.site_url = '/coolbananas/'

api_urls = [
    url(r'^admin/', admin.site.urls),
    url(r'^download/([0-9]+\.[0-9]+\.[0-9]+)/$', download.DownloadTagView.as_view()),
    url(r'^download/$', download.NoTagSpecifiedView.as_view()),
    url(r'^article/(?P<uri>'+URI_PATTERN.pattern+')?$', article.APIArticleView.as_view()),
    url(r'^changelog/$', changelog.ChangeLogView.as_view()),
    url(r'^explorer/$', explorer.ExplorerView.as_view()),
    url(r'^documentation/$', doc.DocView.as_view()),
    url(r'^api/', include(api.urls)),
    url(r'^$', homepage.HomepageView.as_view()),
]

template404 = get_template('assets/api/404.html')

def api404(request, *args, **kwargs):
    exception = kwargs.get('exception')
    exceptionmsg = str(exception) if exception else 'Not Found'
    if isinstance(exception, Resolver404):
        exceptionmsg = 'Invalid URL!'
    content = template404.render({
        'exception': exceptionmsg,
        'path': request.path,
    })
    return HttpResponseNotFound(content, content_type='text/html')