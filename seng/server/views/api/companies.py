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
from ...models import Company, StockExchange
from ....core import logger, sparql
from ....core.constants import RIC_PATTERN

class CompaniesView(SingletonView):

    def __init__(self):
        companies = Company.objects.all()
        exchanges = StockExchange.objects.all()
        companies_to_exchanges = {}
        for ric in sparql.get_rics():
            company, exchange = ric.split('.', 1)
            company_exchanges = companies_to_exchanges.get(company, [])
            company_exchanges.append(exchange)
            companies_to_exchanges[company] = company_exchanges

        def get_company_tuple(company):
            return company.ric, OrderedDict([
                ('InstrumentID', company.ric),
                ('Name', company.name),
                ('Exchanges', OrderedDict(
                    sorted(map(lambda code: (code, self.exchanges[code]), companies_to_exchanges[company.ric]))
                ))
            ])

        try:
            self.exchanges = OrderedDict(sorted(map(lambda exchange: (exchange.code, exchange.name), exchanges)))
            self.companies = OrderedDict(sorted(map(get_company_tuple, companies), key = lambda c: c[0]))
        except:
            self.exchanges = {}
            self.companies = {}
            return

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
                final_json['Companies'] = sorted(self.companies.values(), key = lambda c: c['InstrumentID'])
                final_json['success'] = True
            else:
                ric = ric.upper()
                if ric in self.companies:
                    final_json.update(self.companies[ric])
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
