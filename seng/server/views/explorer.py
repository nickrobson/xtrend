# explorer.py
# SENG3011 - Cool Bananas
#
# Reads the explorer page and presents it.

from django.template.loader import get_template
from django.http import HttpResponse

from ...utils import SingletonView

class ExplorerView(SingletonView):

    def __init__(self):
        template = get_template('assets/api/explorer.html')
        self.content = template.render()

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')