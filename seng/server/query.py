# query.py
# SENG3011 - Cool Bananas
#
# Handles the API's GET request, and should return the JSON object for it.

from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from datetime import datetime
from seng.constants import API_DATE_FORMAT
from seng.sparql import query
from seng.result import to_json
import json

class QueryView(View):
    
    def get(self, request):
        BAD_REQUEST_MESSAGE = '{"errors": [{"status": "400","detail": "Bad request"}]}'

        # First this gets the user's GET request.
        # This is the stuff after the question mark:
        # http://127.0.0.1:5002/coolbananas/api/?rics=BHP.AX,BLT.L&topics=AMERS,COM&startdate=2015-10-01T00:00:00.000Z&enddate=2015-10-10T00:00:00.000Z
        get_query = request.GET
        # Declare this variable for use later.
        final_json = None
        # We need to confirm that the data exists.
        rics = get_query.get('rics', '')
        topics = get_query.get('topics', '')
        # TODO: Is the date given as one date object, or a start and an end date?
        start_date = self.dateQueryToPyFormat(get_query.get('startdate'))
        end_date = self.dateQueryToPyFormat(get_query.get('enddate'))

        if start_date and end_date and len(rics) > 0 and len(topics) > 0:
            # Then extract the data.
            rics = rics.split(',') if len(rics) else []
            topics = topics.split(',') if len(topics) else []
            try:
                # This will still be accepted if not the exact number of decimals is used.
                start_date = datetime.strptime(start_date, API_DATE_FORMAT)
                end_date = datetime.strptime(end_date, API_DATE_FORMAT)
            except:
                return HttpResponseBadRequest(BAD_REQUEST_MESSAGE, content_type="application/json")

            results = query(
                rics = rics,
                topics = topics,
                daterange = (start_date, end_date)
            )

            # This is the final JSON. We need to then return it.
            final_json = to_json(results)
        else:
            return HttpResponseBadRequest(BAD_REQUEST_MESSAGE, content_type="application/json")

        return HttpResponse(json.dumps(final_json), content_type="application/json")

    # This converts a date from the format 2015-10-10T00:00:00.000Z to 2015-10-10T00:00:00:00.000000Z.
    # If the time is not a string, then this should return None.
    def dateQueryToPyFormat(self, date_string):
        if isinstance(date_string, str):
            return date_string[0:-1] + "000Z"
        else:
            return None