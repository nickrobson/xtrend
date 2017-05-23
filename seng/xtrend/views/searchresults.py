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
                        currResult['sentiment'] = newsAPIOutput[i]['Sentiment']['Polarity']
                        lastStock = stockJsonOutput[instrument_id[j]][len(stockJsonOutput[instrument_id[j]]) - 1]
                        currResult['tradingAt'] = lastStock.av_return
                        # currResult['lastReturn'] = 
                        searchResults.append(currResult)

        print(searchResults)


        # searchOutput = []
        # for ric in newsAPIOutput:
        #     stockJsonOutput = stocks.get(ric, 
        #         upper_window,
        #         lower_window, 
        #         doi)
        #     if newsAPIOutput.sentiment < 0 && buy
        #         or sentiment > 1 and sell
        #     if sentiment is pos / neg as appropriate
        #     and 

        #     /*
       

        # urlResults = "";
        # urlResults = urlResults + "numResults=" + resultsJson.length;
        # console.log("hi");
        # for (i = 0; i < resultsJson.length; i++) {
        #     urlResults = urlResults + "&company=" + resultsJson[i].company
        #     + "&exchange=" + resultsJson[i].exchange
        #     + "&sentiment=" + resultsJson[i].sentiment
        #     + "&tradingAt=" + resultsJson[i].tradingAt
        #     + "&lastReturn=" + resultsJson[i].lastReturn
        # }

        # // loop through resultsJson and make a url string
        # //window.location.href = "/coolbananas/xtrend/search/results?" + urlResults;
        # return "/coolbananas/xtrend/search/results?" + urlResults;

        # self.content = self.template.render({
        #     'range': range(0, int(request.GET.get('numResults'))),
        #     'company': request.GET.getlist('company'),
        #     'exchange': request.GET.getlist('exchange'),
        #     'sentiment': request.GET.getlist('sentiment'),
        #     'tradingAt': request.GET.getlist('tradingAt'),
        #     'lastReturn': request.GET.getlist('lastReturn')
        # })

        # self.content = self.template.render({
        #     'range': range(0, int(request.GET.get('numResults'))),
        #     'company': request.GET.getlist('company'),
        #     'exchange': request.GET.getlist('exchange'),
        #     'sentiment': request.GET.getlist('sentiment'),
        #     'tradingAt': request.GET.getlist('tradingAt'),
        #     'lastReturn': request.GET.getlist('lastReturn')
        # });
        self.content = self.template.render();
        return HttpResponse(self.content, content_type='text/html')

    
