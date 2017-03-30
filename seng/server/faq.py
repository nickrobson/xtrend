# faq.py
# SENG3011 - Cool Bananas
#
# Reads the FAQ page and presents it.

from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View

# TODO: Should we merge this and ChangelogView into one common class?
class FaqView(View):
    def __init__(self):
        self.content = ''
        with open('assets/faq.html') as f:
            self.content = f.read()

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')
