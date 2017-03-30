import os

from django.http import FileResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import redirect

from ...core import gitutils

class DownloadTagView(View):

    def get(self, request, tag):
        tag = tag.replace(".", "_")
        file = os.path.join('.tags', tag + '.tar.gz')
        if not os.path.isfile(file):
            return HttpResponseBadRequest('<html><head><title>No such tag</title></head><body><h1>No such tag!</h1></body></html>', content_type='text/html')
        response = FileResponse(open(file, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="Cool_Bananas_%s"' % (os.path.basename(file),)
        return response

class NoTagSpecifiedView(View):

    def __init__(self):
        tags = gitutils.get_git_tags()
        self._latest_tag = tags[-1]

    def get(self, request):
        return redirect('/coolbananas/tag/%s' % (self._latest_tag,))
