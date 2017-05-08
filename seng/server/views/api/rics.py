# rics.py
# SENG3011 - Cool Bananas
#
# Allows getting a list of RICs

import json

from collections import OrderedDict
from django.http import HttpResponse
from django.utils import timezone

from .utils import err
from .. import SingletonView
from ....core import logger, sparql

class RicsView(SingletonView):

    def __init__(self):
        self.rics = sparql.get_rics()

    def get(self, request):
        exec_start_date = timezone.now()
        logger.info('Execution started at', exec_start_date)
        def end_exec():
            exec_end_date = timezone.now()
            logger.info('Execution ended at', exec_end_date)
            logger.info('Execution completed in', exec_end_date - exec_start_date)
        try:
            final_json = OrderedDict()
            final_json['InstrumentIDs'] = self.rics
            final_json['success'] = True
            end_exec()
            return HttpResponse(json.dumps(final_json), content_type="application/json")
        except Exception as e:
            logger.exception(e)
            end_exec()
            return err(str(e))
