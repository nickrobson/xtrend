# homepage.py
# SENG3011 - Cool Bananas
#
# Displays homepage with list of revisions of code

from django.template.loader import get_template
from django.http import HttpResponse, QueryDict, Http404

from ...utils import SingletonView

from datetime import date, timedelta

from ..core import stocks, rating
from seng.server import cache


class SearchResultsView(SingletonView):
    
    def __init__(self):
        self.template = get_template('assets/xtrend/searchresults.html')
        
    def get(self, request):
        searchRics = request.GET.get('instrument_id', '').strip()
        if not len(searchRics):
            raise Http404('You need to specify some companies to search for!')
        searchRics = searchRics.split(',')

        searchMode = request.GET.get('mode')
        if searchMode not in ('sell', 'buy'):
            raise Http404('Invalid search mode!')

        try:
            searchRange = int(request.GET.get('range'))
        except:
            raise Http404('Invalid range given!')

        currentDate = date(2015, 12, 31)

        searchResults = []
        not_included = []

        for ric in searchRics:
            ricRating = rating.get_rating(ric)
            lower_window = 10
            upper_window = 0
            stockJsonOutput = stocks.get(
                [ric],
                upper_window,
                lower_window,
                currentDate
            )
            lastStock = None
            for stock in reversed(stockJsonOutput[ric]):
                if stock.adjusted_close >= 0:
                    lastStock = stock
                    break
            if lastStock is None:
                not_included.append('{} was not included in the search results as no price data is available for it.'.format(ric))
                continue
            price = lastStock.adjusted_close
            if ((searchMode == 'sell' and ricRating <= 0 and price >= searchRange)
                    or (searchMode == 'buy' and ricRating >= 0 and price <= searchRange)):
                searchResults.append({
                    'instrument_id': ric,
                    'sentiment': '{0:0.4f}'.format(ricRating),
                    'tradingAt': '{0:0.3f}'.format(lastStock.adjusted_close),
                    'lastReturn': '{0:0.3f}'.format(lastStock.return_value),
                    'ratingPercentage': '{0:0.1f}'.format((ricRating + 100) / 2),
                })
            else:
                if searchMode == 'sell' and ricRating >= 0:
                    no_results_message = "{}'s rating is positive, which would suggest that you buy it - not sell it.".format(ric)
                elif searchMode == 'buy' and ricRating <= 0:
                    no_results_message = "{}'s rating is negative, which would suggest that you sell it - not buy it.".format(ric)
                else:
                    quantifier = 'only ' if searchMode == 'sell' else ''
                    lt_or_gt = 'less' if searchMode == 'sell' else 'greater'
                    no_results_message = "{}'s stock price is {}${:.2f}, which is {} than your cut-off of ${}.".format(ric, quantifier, price, lt_or_gt, searchRange)
                not_included.append(no_results_message)

        self.content = self.template.render({
            'SearchResults': searchResults,
            'NotIncluded': not_included,
            'QueryString': request.GET.urlencode(),
        });

        return HttpResponse(self.content, content_type='text/html')

    
