import os

from django.http import FileResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import redirect

from ..core import gitutils

class DownloadTagView(View):

    def get(self, request, tag):
        tag = tag.replace(".", "_")
        file = os.path.join('.tags', tag + '.tar.gz')
        if not os.path.isfile(file):
            return HttpResponseBadRequest('<html><head><title>No such tag</title></head><body><h1>No such tag!</h1></body></html>', content_type='text/html')
        response = FileResponse(open(file, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % (os.path.basename(file),)
        return response

class NoTagSpecifiedView(View):

    def get(self, request):
        tags = gitutils.get_git_tags()
        return redirect('/coolbananas/tag/%s' % (tags[-1],))
