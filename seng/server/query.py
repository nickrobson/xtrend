# query.py
# SENG3011 - Cool Bananas
#
# Handles the API's GET request, and should return the JSON object for it.

import json
import pytz
import time

from collections import OrderedDict
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from datetime import datetime
from seng import logger, cache
from seng.constants import API_DATE_FORMAT, RIC_LIST_PATTERN, _RIC_PATTERN
from seng.sparql import query
from seng.result import to_json

def get_error_json(message):
    return json.dumps(OrderedDict([
            ('error', message),
            ('success', False)
        ]))

def err(message):
    return HttpResponseBadRequest(get_error_json(message), content_type='application/json')

class QueryView(View):
    
    def get(self, request):
        try:

            start_time = time.clock()

            # First this gets the user's GET request.
            # This is the stuff after the question mark:
            # http://127.0.0.1:5002/coolbananas/api/?rics=BHP.AX,BLT.L&topics=AMERS,COM&startdate=2015-10-01T00:00:00.000Z&enddate=2015-10-10T00:00:00.000Z
            get_query = request.GET
            # We need to confirm that the data exists.
            rics = get_query.get('rics', '')
            topics = get_query.get('topics', '')
            uniq = get_query.get('uniq', '').lower() == 'true'
            # TODO: Is the date given as one date object, or a start and an end date?
            start_date = get_query.get('startdate', '')
            end_date = get_query.get('enddate')

            if len(rics) and not RIC_LIST_PATTERN.fullmatch(rics):
                return err('Invalid RICs list (must match regex of %s)' % RIC_LIST_PATTERN.pattern)

            if len(topics) and not RIC_LIST_PATTERN.fullmatch(topics):
                return err('Invalid topic codes list (must match regex of %s)' % RIC_LIST_PATTERN.pattern)

            if start_date and end_date:
                # Then extract the data.
                rics = rics.split(',') if len(rics) else []
                topics = topics.split(',') if len(topics) else []
                try:
                    start_date = datetime.strptime(start_date, API_DATE_FORMAT).replace(tzinfo=pytz.UTC)
                except:
                    return err('Invalid start date format, must match: %s, not %s' % (API_DATE_FORMAT, start_date))
                try:
                    end_date = datetime.strptime(end_date, API_DATE_FORMAT).replace(tzinfo=pytz.UTC)
                except:
                    return err('Invalid end date format, must match: %s, not %s' % (API_DATE_FORMAT, end_date))

                if start_date > end_date:
                    return err('Start date is after end date')

                logger.debug('Received query for: RICs = %s, Topics = %s, Dates = %s' % (rics, topics, (start_date, end_date)))

                final_json = cache.query(
                    rics = rics,
                    topics = topics,
                    date_range = (start_date, end_date),
                    uniq = uniq,
                )
                end_time = time.clock()

                final_json['success'] = True
                final_json['query_time'] = end_time - start_time

                logger.debug('Query handled in %.8f seconds' % (end_time - start_time))
                return HttpResponse(json.dumps(final_json), content_type="application/json")
            elif not start_date:
                return err('Missing start date')
            elif not end_date:
                return err('Missing end date')
            return err('Missing fields')
        except Exception as e:
            logger.exception(e)
            return err(str(e))

class ExplorerView(View):

    def __init__(self):
        self.content = ''
        with open('assets/explorer.html') as f:
            self.content = f.read()

    def get(self, request):
        return HttpResponse(self.content, content_type='text/html')
