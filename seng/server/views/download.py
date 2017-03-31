import os
import subprocess

from django.http import FileResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect

from . import SingletonView
from ...core import gitutils

class DownloadTagView(SingletonView):

    def __init__(self):
        self.tags = gitutils.get_git_tags()

    def get(self, request, tag):
        tag = tag.replace(".", "_")
        file = os.path.join('.tags', tag + '.tar.gz')
        if not os.path.isfile(file) and tag in self.tags:
            exit_code = subprocess.call(['git', 'archive', '--format=tar.gz', '-o', file, tag])
            if exit_code != 0:
                return HttpResponseServerError('<html><head><title>Failed to create archive</title></head><body>Tag found, but the server failed to create the archive</body></html>', content_type='text/html')
        if not os.path.isfile(file):
            return HttpResponseBadRequest('<html><head><title>No such tag</title></head><body><h1>No such tag!</h1></body></html>', content_type='text/html')
        response = FileResponse(open(file, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="Cool_Bananas_%s"' % (os.path.basename(file),)
        return response

class NoTagSpecifiedView(SingletonView):

    def __init__(self):
        tags = gitutils.get_git_tags()
        self._latest_tag = tags[-1].replace('_', '.')

    def get(self, request):
        return redirect('/coolbananas/download/%s' % (self._latest_tag,))
