# base.py
# SENG3011 - Cool Bananas
#
# Handles the API's GET requests, and returns the JSON response for them.

import json
import pytz
import time

from collections import OrderedDict
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime

from .utils import err, get_error_json
from .. import SingletonView
from ... import cache
from ....core import logger
from ....core.constants import API_DATE_FORMAT, RIC_LIST_PATTERN, TOPIC_LIST_PATTERN


class ApiView(SingletonView):

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
            rics = get_query.pop('InstrumentIDs', '')
            topics = get_query.pop('TopicCodes', '')
            start_date = get_query.pop('StartDate', '')
            end_date = get_query.pop('EndDate', '')
            sentiment = get_query.pop('Sentiment', '0') == '1'

            if len(get_query):
                end_exec()
                return err('Invalid query parameters: %s' % (', '.join(get_query),))

            if len(rics) and not RIC_LIST_PATTERN.fullmatch(rics):
                end_exec()
                return err('Invalid RICs list (must match regex of %s)' % RIC_LIST_PATTERN.pattern)

            if len(topics) and not TOPIC_LIST_PATTERN.fullmatch(topics):
                end_exec()
                return err('Invalid topic codes list (must match regex of %s)' % TOPIC_LIST_PATTERN.pattern)
            if not start_date and not end_date:
                end_exec()
                return err('Missing StartDate and EndDate')
            elif not start_date:
                end_exec()
                return err('Missing StartDate')
            elif not end_date:
                end_exec()
                return err('Missing EndDate')

            # Dates are present (they need to be)
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
                end_exec()
                return err('StartDate is after EndDate')

            logger.debug('Received query for: RICs = %s, Topics = %s, Dates = %s' % (rics, topics, (start_date, end_date)))

            cache_results = cache.query(
                rics = rics,
                topics = topics,
                date_range = (start_date, end_date),
            )
            end_time = time.clock()

            if len(rics) or len(topics):
                for result in cache_results:
                    if len(rics):
                        result['InstrumentIDs'] = list(filter(lambda r: r in rics, result['InstrumentIDs']))
                    if len(topics):
                        result['TopicCodes'] = list(filter(lambda t: t in topics, result['TopicCodes']))

            if not sentiment:
                for result in cache_results:
                    del result['Sentiment']

            final_json = OrderedDict()
            final_json['NewsDataSet'] = cache_results
            final_json['query_time'] = end_time - start_time
            final_json['success'] = True

            end_exec()
            return HttpResponse(json.dumps(final_json), content_type="application/json")
        except Exception as e:
            logger.exception(e)
            end_exec()
            return err(str(e))
