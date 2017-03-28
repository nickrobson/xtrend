# query.py
# SENG3011 - Cool Bananas
#
# Displays homepage with list of revisions of code

from django.template.loader import get_template
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest


from ..core import gitutils

import subprocess


class HomepageView(View):
    def __init__(self):
        self.content = ''
        template = get_template('assets/demo-webpage.html')
        with subprocess.Popen(["git", "tag", "-l"], stdout=subprocess.PIPE) as proc:
            verList = proc.stdout.read().decode("utf-8").splitlines()

        versionList = gitutils.get_git_tags()

        versions = []
        for versionNumber in versionList:
            version = {
                'number': versionNumber,
                'link': "https://github.com/nickrobson/SENG3011/tree/" + versionNumber,
                'tagDescription': gitutils.get_description(versionNumber),
                #'downloadLink': ??
            }
            versions.append(version)
        self.content = template.render({'versions': versions})

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')

