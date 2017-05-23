# homepage.py
# SENG3011 - Cool Bananas
#
# Displays homepage with list of revisions of code

from django.template.loader import get_template
from django.http import HttpResponse

from ...utils import SingletonView

class SearchResultsView(SingletonView):
    
    def __init__(self):
        self.template = get_template('assets/xtrend/searchresults.html')
        #self.content = template.render()
        

    def get(self, request):
        self.content = self.template.render({
            'range': range(0, int(request.GET.get('numResults'))),
            'company': request.GET.getlist('company'),
            'exchange': request.GET.getlist('exchange'),
            'sentiment': request.GET.getlist('sentiment'),
            'tradingAt': request.GET.getlist('tradingAt'),
            'lastReturn': request.GET.getlist('lastReturn')
        });
        return HttpResponse(self.content, content_type='text/html')

    
