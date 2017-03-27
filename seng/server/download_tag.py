import os

from django.http import FileResponse, Http404
from django.views import View

class DownloadTagView(View):

    def get(self, request, tag):
        file = os.path.join('.tags', tag + '.tar.gz')
        if not os.path.isfile(file):
            raise Http404
        response = FileResponse(open(file, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % (os.path.basename(file),)
        return response
