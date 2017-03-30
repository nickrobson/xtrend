# query.py
# SENG3011 - Cool Bananas
#
# Displays homepage with list of revisions of code

from django.template.loader import get_template
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest

from ...core import gitutils

import subprocess
import markdown
from markdown.extensions.smarty import SmartyExtension

class HomepageView(View):
    def __init__(self):
        versionList = gitutils.get_git_tags()
        mk = markdown.Markdown([ SmartyExtension() ])
        versions = []
        reversedVersions = list(versionList[::-1])
        for version in reversedVersions:
            display_version = version.replace("_", ".")
            version_data = {
                'version': version,
                'display': display_version,
                'github': "https://github.com/nickrobson/SENG3011/tree/" + version,
                'download': "/coolbananas/download/" + display_version,
                'description': mk.convert(gitutils.get_description(version))
            }
            versions.append(version_data)

        template = get_template('assets/homepage.html')
        self.content = template.render({'versions': versions})

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')

