# dates.py
# SENG3011 - Cool Bananas
#
# Allows getting a list of dates/datetimes

import json

from collections import OrderedDict
from django.http import HttpResponse
from django.utils import timezone
from datetime import date, datetime

from .utils import err
from .. import SingletonView
from ....core import logger, sparql
from ....core.constants import DATE_FORMAT, API_DATE_FORMAT

class DatesView(SingletonView):

    def __init__(self):
        self.dates = list(map(lambda d: d.strftime(DATE_FORMAT), sparql.get_dates()))
        self.datetimes = list(map(lambda d: d.strftime(API_DATE_FORMAT), sparql.get_datetimes()))

    def get(self, request):
        show_times = 'time' in request.GET
        exec_start_date = timezone.now()
        logger.info('Execution started at', exec_start_date)
        def end_exec():
            exec_end_date = timezone.now()
            logger.info('Execution ended at', exec_end_date)
            logger.info('Execution completed in', exec_end_date - exec_start_date)
        try:
            final_json = OrderedDict()
            final_json['Datetimes' if show_times else 'Dates'] = self.datetimes if show_times else self.dates
            final_json['success'] = True
            end_exec()
            return HttpResponse(json.dumps(final_json), content_type="application/json")
        except Exception as e:
            logger.exception(e)
            end_exec()
            return err(str(e))
