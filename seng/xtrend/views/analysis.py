# homepage.py
# SENG3011 - Cool Bananas
#
# Displays homepage with list of revisions of code

from django.template.loader import get_template
from django.http import HttpResponse

from ...utils import SingletonView

class RICAnalysisView(SingletonView):

    def __init__(self):
        template = get_template('assets/xtrend/analysis.html')
        self.content = template.render()

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')

