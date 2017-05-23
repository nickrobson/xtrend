# homepage.py
# SENG3011 - Cool Bananas
#
# Displays homepage with list of revisions of code

from django.template.loader import get_template
from django.http import HttpResponse
from django.http import QueryDict

from ...utils import SingletonView

from datetime import date, timedelta

from ..core import stocks
from seng.server import cache

class SearchResultsView(SingletonView):
    
    def __init__(self):
        self.template = get_template('assets/xtrend/searchresults.html')
        #self.content = template.render()
        

    def get(self, request):
        resultsJson = [];
        
        # // TODO(anna):
        # /*
        # given what they search for:
        # get all things from our api where 
        #     ric = ric
        # and
        #     sentiment within buy/ sell
        #         sort by this?
        #     for this get:
        #         data from stock api
        #         where lastReturn within threshold

        # */

        # for each ric:
        searchRics = request.GET.getlist('instrument_id')
        searchBuy = request.GET.get('buy')
        searchSell = request.GET.get('sell')
        searchRangeLow = request.GET.get('range_low')
        searchRangeHi = request.GET.get('range_hi')
        searchDays = request.GET.get('days')

        currentDate = date(2015, 12, 31)
        date_range = [
            currentDate - timedelta(days = int(searchDays)),
            currentDate
        ]
        newsAPIOutput = cache.query(searchRics, [], date_range);

        searchResults = []
        numResults = 0
        for i in range(0, len(newsAPIOutput)):
            instrument_id = newsAPIOutput[i]['InstrumentIDs']
            print("hi")
            print(instrument_id)
            lower_window = 0
            upper_window = int(searchDays)
            stockJsonOutput = stocks.get(
                instrument_id,
                upper_window,
                lower_window,
                currentDate #doi
            )
            sentiment = newsAPIOutput[i]['Sentiment']['Polarity']
            if ((searchBuy == "1" and sentiment > 0)
                or (searchSell == "1" and sentiment < 0)):
                # print("sentiment:")
                #print(sentiment)
                for j in range (0, len(instrument_id)):
                    #print(stockJsonOutput[instrument_id[j]][0])
                    if (len(stockJsonOutput[instrument_id[j]]) > 0):
                        currResult = {}
                        currResult['instrument_id'] = instrument_id[j]
                        currResult['sentiment'] = newsAPIOutput[i]['Sentiment']['Polarity']
                        lastStock = stockJsonOutput[instrument_id[j]][len(stockJsonOutput[instrument_id[j]]) - 1]
                        currResult['tradingAt'] = lastStock.av_return
                        currResult['lastReturn'] = 0 #fix
                        searchResults.append(currResult)
                        numResults += 1

        print(searchResults)


        self.content = self.template.render({
            'range': range(0, numResults),
            'searchResults': searchResults
        });

        return HttpResponse(self.content, content_type='text/html')

    
