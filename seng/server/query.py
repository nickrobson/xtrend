# query.py
# SENG3011 - Cool Bananas
#
# Handles the API's GET request, and should return the JSON object for it.

from django.http import HttpResponse
from django.views import View
from datetime import datetime
from seng.constants import DB_DATE_FORMAT
from seng.sparql import query
from seng.result import to_json
import json

class QueryView(View):
    
    def get(self, request):
        # First this gets the user's GET request.
        # This is the stuff after the question mark:
        # http://127.0.0.1:5002/coolbananas/api/?ric=BHP.AX,BLT.L&topics=AMERS,COM&startdate=2015-10-01T00:00:00Z&enddate=2015-10-10T00:00:00Z
        getQuery = request.GET
        # Then extracts the data.
        rics = getQuery.get('ric').split(',')
        topics = getQuery.get('topics').split(',')
        # TODO: Is the date given as one date object, or a start and an end date?
        startDate = getQuery.get('startdate')
        endDate = getQuery.get('enddate')

        # TODO: Add None checking.

        results = query(
            rics = rics,
            topics = topics,
            daterange = (datetime.strptime(startDate, DB_DATE_FORMAT), datetime.strptime(endDate, DB_DATE_FORMAT))
        )

        # This is the final JSON. We need to then return it.
        finalJson = to_json(results)

        return HttpResponse(json.dumps(finalJson), content_type="application/json")