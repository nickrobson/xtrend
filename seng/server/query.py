# query.py
# SENG3011 - Cool Bananas
#
# Handles the API's GET request, and should return the JSON object for it.

import json
import pytz
import time

from collections import OrderedDict
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template
from django.views import View
from django.utils import timezone
from datetime import datetime
import re

from . import cache
from ..core import logger
from ..core.constants import API_DATE_FORMAT, RIC_LIST_PATTERN, _RIC_PATTERN
from ..core.sparql import query
from ..core.result import to_json

import subprocess


def get_error_json(message):
    return json.dumps(OrderedDict([
            ('error', message),
            ('success', False)
        ]))


def err(message):
    return HttpResponseBadRequest(get_error_json(message), content_type='application/json')


class QueryView(View):

    def get(self, request):
        exec_start_date = timezone.now()
        logger.info('Execution started at', exec_start_date)
        def end_exec():
            exec_end_date = timezone.now()
            logger.info('Execution ended at', exec_end_date)
            logger.info('Execution completed in', exec_end_date - exec_start_date)
        try:
            start_time = time.clock()

            # First this gets the user's GET request.
            # This is the stuff after the question mark:
            # http://127.0.0.1:5002/coolbananas/api/?InstrumentIDs=BHP.AX,BLT.L&TopicCodes=AMERS,COM&StartDate=2015-10-01T00:00:00.000Z&EndDate=2015-10-10T00:00:00.000Z
            get_query = request.GET.dict()
            # We need to confirm that the data exists.
            rics = get_query.pop('InstrumentIDs', '')
            topics = get_query.pop('TopicCodes', '')
            start_date = get_query.pop('StartDate', '')
            end_date = get_query.pop('EndDate', '')

            if len(get_query):
                end_exec()
                return err('Invalid query parameters: %s' % (', '.join(list(get_query)),))

            if len(rics) and not RIC_LIST_PATTERN.fullmatch(rics):
                end_exec()
                return err('Invalid RICs list (must match regex of %s)' % RIC_LIST_PATTERN.pattern)

            if len(topics) and not RIC_LIST_PATTERN.fullmatch(topics):
                end_exec()
                return err('Invalid topic codes list (must match regex of %s)' % RIC_LIST_PATTERN.pattern)

            if start_date and end_date:
                # Then extract the data.
                rics = rics.split(',') if len(rics) else []
                topics = topics.split(',') if len(topics) else []
                try:
                    start_date = datetime.strptime(start_date, API_DATE_FORMAT).replace(tzinfo=pytz.UTC)
                except:
                    end_exec()
                    return err('Invalid start date format, must match: %s, not %s' % (API_DATE_FORMAT, start_date))
                try:
                    end_date = datetime.strptime(end_date, API_DATE_FORMAT).replace(tzinfo=pytz.UTC)
                except:
                    end_exec()
                    return err('Invalid end date format, must match: %s, not %s' % (API_DATE_FORMAT, end_date))

                if start_date > end_date:
                    return err('Start date is after end date')

                logger.debug('Received query for: RICs = %s, Topics = %s, Dates = %s' % (rics, topics, (start_date, end_date)))

                final_json = cache.query(
                    rics = rics,
                    topics = topics,
                    date_range = (start_date, end_date),
                )
                end_time = time.clock()

                final_json['success'] = True
                final_json['query_time'] = end_time - start_time

                end_exec()
                return HttpResponse(json.dumps(final_json), content_type="application/json")
            elif not start_date:
                end_exec()
                return err('Missing start date')
            elif not end_date:
                end_exec()
                return err('Missing end date')
            end_exec()
            return err('Missing fields')
        except Exception as e:
            logger.exception(e)
            end_exec()
            return err(str(e))


class ExplorerView(View):

    def __init__(self):
        self.content = ''
        with open('assets/explorer.html') as f:
            self.content = f.read()

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')

class HomepageView(View):
    def __init__(self):
        self.content = ''
        template = get_template('assets/demo-webpage.html')
        with subprocess.Popen(["git", "tag", "-l"], stdout=subprocess.PIPE) as proc:
            verList = proc.stdout.read().decode("utf-8").splitlines()
        versions = []
        for ver in verList:
            with subprocess.Popen(["git", "show", ver], stdout=subprocess.PIPE) as proc:
                tagShow = proc.stdout.read().decode("utf-8")
            #some funky manipluation to get just commit msg:
            tagShow = re.sub("tag " + ver
                + "\s*Tagger:.*\s*Date:[^\n]*", "", tagShow)
            tagstring = tagShow.split('commit')
            tagShow = tagstring[0]

            version = {
                'number': ver,
                'link': "https://github.com/nickrobson/SENG3011/tree/" + ver,
                'tagDescription': tagShow,
                #'downloadLink': ??
            }
            versions.append(version)
        self.content = template.render({'versions': versions})

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')



