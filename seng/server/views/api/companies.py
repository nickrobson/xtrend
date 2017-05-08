# companies.py
# SENG3011 - Cool Bananas
#
# Allows getting a list of companies

import json

from collections import OrderedDict
from django.http import HttpResponse
from django.utils import timezone

from .utils import err
from .. import SingletonView
from ...models import Company
from ....core import logger, sparql
from ....core.constants import RIC_PATTERN

class CompaniesView(SingletonView):

    def __init__(self):
        self.companies = Company.objects.all()
        self.companies = OrderedDict(sorted(map(lambda c: (c.ric, c.name), self.companies)))
        self.companies_to_exchanges = {}
        for ric in sparql.get_rics():
            company, exchange = ric.split('.', 1)
            exchanges = self.companies_to_exchanges.get(company, [])
            exchanges.append(exchange)
            self.companies_to_exchanges[company] = exchanges

    def get(self, request, ric = None):
        exec_start_date = timezone.now()
        logger.info('Execution started at', exec_start_date)
        def end_exec():
            exec_end_date = timezone.now()
            logger.info('Execution ended at', exec_end_date)
            logger.info('Execution completed in', exec_end_date - exec_start_date)
        try:
            final_json = OrderedDict()
            if ric is None:
                final_json['Companies'] = self.companies
                final_json['success'] = True
            else:
                ric = ric.upper()
                if ric in self.companies:
                    final_json['InstrumentID'] = ric.upper()
                    final_json['Name'] = self.companies[ric]
                    final_json['Exchanges'] = self.companies_to_exchanges[ric]
                    final_json['success'] = True
                else:
                    final_json['error'] = 'Invalid RIC: not applicable'
                    final_json['success'] = False
            end_exec()
            return HttpResponse(json.dumps(final_json), content_type="application/json")
        except Exception as e:
            logger.exception(e)
            end_exec()
            return err(str(e))
