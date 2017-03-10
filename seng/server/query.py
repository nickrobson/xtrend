from django.http import HttpResponse
from django.views import View

class QueryView(View):
    
    def get(self, request):
        return HttpResponse('// todo')

        