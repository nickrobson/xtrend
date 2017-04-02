# homepage.py
# SENG3011 - Cool Bananas
#
# Displays homepage with list of revisions of code

from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseBadRequest

from . import SingletonView
from ...core import gitutils, mk

def _get_git_data(tag):
    display_version = tag.replace("_", ".")
    tag_metadata = gitutils.get_tag_meta(tag)
    version_data = {
        'version': tag,
        'display': display_version,
        'github': "https://github.com/nickrobson/SENG3011/tree/" + tag,
        'download': "/coolbananas/download/" + display_version,
        'description': mk.convert(tag_metadata['description']),
        'date': tag_metadata['date'].strftime('%d/%m/%y')
    }
    return version_data

class HomepageView(SingletonView):

    def __init__(self):
        versions = list(map(_get_git_data, reversed(gitutils.get_tags())))
        template = get_template('assets/homepage.html')
        self.content = template.render({'versions': versions})

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')

