# changelog.py
# SENG3011 - Cool Bananas
#
# Reads the changelog page and presents it.

from datetime import datetime
from django.template.loader import get_template
from django.http import HttpResponse

from . import SingletonView
from ...core import gitutils

def _get_git_data(tag):
    display_version = tag.replace("_", ".")
    tag_metadata = gitutils.get_tag_meta(tag)
    version_data = {
        'version': tag,
        'display': display_version,
        'changes': tag_metadata['description'].split('\n\n'),
        'date': tag_metadata['date'].strftime('%d/%m/%y')
    }
    return version_data

class ChangeLogView(SingletonView):

    def __init__(self):
        versions = list(map(_get_git_data, reversed(gitutils.get_tags())))
        template = get_template('assets/changelog.html')
        self.content = template.render({'versions': versions})

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')
