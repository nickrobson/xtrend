from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View

class ExplorerView(View):

    def __init__(self):
        template = get_template('assets/explorer.html')
        self.content = template.render()

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')