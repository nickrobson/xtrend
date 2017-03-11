# query.py
# SENG3011 - Cool Bananas
#
# Handles the API's GET request, and should return the JSON object for it.

from django.http import HttpResponse, HttpResponseBadRequest
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
        # http://127.0.0.1:5002/coolbananas/api/?rics=BHP.AX,BLT.L&topics=AMERS,COM&startdate=2015-10-01T00:00:00Z&enddate=2015-10-10T00:00:00Z
        get_query = request.GET
        # Declare this variable for use later.
        final_json = None
        # We need to confirm that the data exists.
        if get_query.get('rics') and get_query.get('topics') and get_query.get('startdate') and get_query.get('enddate'):
            # Then extract the data.
            rics = get_query.get('rics').split(',')
            topics = get_query.get('topics').split(',')
            # TODO: Is the date given as one date object, or a start and an end date?
            start_date = get_query.get('startdate')
            end_date = get_query.get('enddate')

            # TODO: Additional type checks?

            results = query(
                rics = rics,
                topics = topics,
                daterange = (datetime.strptime(start_date, DB_DATE_FORMAT), datetime.strptime(end_date, DB_DATE_FORMAT))
            )

            # This is the final JSON. We need to then return it.
            final_json = to_json(results)
        else:
            return HttpResponseBadRequest('{"errors": [{"status": "400","detail": "Bad request"}]}', content_type="application/json")

        return HttpResponse(json.dumps(final_json), content_type="application/json")