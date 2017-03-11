# sparql.py
# SENG3011 - Cool Bananas
#
# Functions used for converting user input into SPARQL, and querying the master database.

import base64
import json
import urllib.parse
import urllib.request

from datetime import datetime

from .result import QueryResult
from .constants import QUERY_TEMPLATE, DB_DATE_FORMAT

# Converts the submitted RIC string into the format required for the SPARQL.
def get_ric_filter(rics):
    if len(rics) == 0:
        return ''
    each = map('?ric = ins:RIC_{}'.format, rics)
    cond = ' || '.join(each)
    return 'FILTER (%s)' % cond

# Converts the submitted topic filters into the format required for the SPARQL.
def get_topic_filter(topics):
    if len(topics) == 0:
        return ''
    each = map('?topicCode = "N2:{}"'.format, topics)
    cond = ' || '.join(each)
    return 'FILTER (%s)' % cond

# Converts the submitted dates into the format required for the SPARQL.
def get_date_filter(start, end):
    mapper = lambda d: '"{}"^^xs:dateTime'.format(d.strftime(DB_DATE_FORMAT))
    cond_format = 'xs:dateTime(?time) > %s && xs:dateTime(?time) <= %s'
    cond = cond_format % tuple(map(mapper, [start, end]))
    return 'FILTER (%s)' % cond

# Takes lists of the input RICs, topics, and dates, and converts it all into a SPARQL request.
def query(rics=[], topics=[], date_range=[]):
    r = get_ric_filter(rics)
    t = get_topic_filter(topics)
    d = get_date_filter(*date_range)

    q = QUERY_TEMPLATE.format(filter_ric=r, filter_topic=t, filter_daterange=d)

    return do_query(q)

# Asks the external database using a given SPARQL query, and returns the result.
def do_query(query):
    encoded = urllib.parse.quote(query.strip())
    req = urllib.request.Request('http://adage.cse.unsw.edu.au:8005/v1/graphs/sparql?query=' + encoded)
    req.add_header('Authorization', 'Basic ' + base64.b64encode(b'student:studentML').decode('utf-8'))
    results = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    results = results['results']['bindings']
    # This is a set that turns all the results through the function QueryResult.
    # It is not a hash map, it's just a set.
    return set(map(QueryResult, results))
