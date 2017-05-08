# sparql.py
# SENG3011 - Cool Bananas
#
# Functions used for converting user input into SPARQL, and querying the master database.

# RACE CONDITION EXPLANATION:
# ---------------------------
# When there is a FILTER statement with one condition (no || or &&),
#   the database software (for some reason) ignores the condition entirely
#   and instead matches it as 'FALSE'. Hence no results are returned!
# The crude fix for this is to add an extra condition that is NEVER true.
#   for this case we use the dummy "qwertyuiop" which is neither a valid RIC
#   nor a valid topic code. Hence it will never match it, only the first condition.

import base64
import json
import urllib.parse
import urllib.request

from datetime import date, datetime

from . import logger
from .result import QueryResultSet
from .constants import *

RICS_LIST, TOPICS_LIST, DATES_LIST, DATETIMES_LIST = [], [], [], []

def _load_db_data():
    global RICS_LIST, TOPICS_LIST, DATETIMES_LIST, DATES_LIST

    data = query_db(LIST_RICS_QUERY)
    data = map(lambda o: o['ric']['value'], data)
    rics = set(map(lambda o: o[o.rfind('RIC_')+4:].upper(), data))
    RICS_LIST = sorted(filter(RIC_PATTERN.fullmatch, rics))

    data = query_db(LIST_TOPICS_QUERY)
    data = map(lambda o: o['topicCode']['value'], data)
    topics = set(map(lambda o: o[o.rfind('N2:')+3:].upper(), data))
    TOPICS_LIST = sorted(filter(TOPIC_PATTERN.fullmatch, topics))

    data = query_db(LIST_DATES_QUERY)
    data = map(lambda o: o['time']['value'], data)
    DATETIMES_LIST = sorted(set(map(lambda d: datetime.strptime(d, API_DATE_FORMAT), data)))

    DATES_LIST = sorted(set(map(datetime.date, get_datetimes())))

# Converts the submitted RIC string into the format required for the SPARQL.
def get_ric_filter(rics):
    if len(rics) == 0:
        return ''
    each = map('?ric = ins:RIC_{}'.format, rics)
    cond = ' || '.join(each)
    return 'FILTER (%s || ?ric = ins:RIC_qwertyuiop)' % cond # the last condition is to fix the race condition explained above


# Converts the submitted topic filters into the format required for the SPARQL.
def get_topic_filter(topics):
    if len(topics) == 0:
        return ''
    each = map('?topicCode = "N2:{}"'.format, topics)
    cond = ' || '.join(each)
    return 'FILTER (%s || ?topicCode = "N2:qwertyuiop")' % cond # the last condition is to fix the race condition explained above

# Converts the submitted dates into the format required for the SPARQL.
def get_date_filter(start, end):

    def mapper(d):
        return '"{}"^^xs:dateTime'.format(d.strftime(DB_DATE_FORMAT))

    cond_format = 'xs:dateTime(?time) > %s && xs:dateTime(?time) <= %s'
    cond = cond_format % tuple(map(mapper, [start, end]))
    return 'FILTER (%s)' % cond

# Asks the external database using a given SPARQL query, and returns the result.
def query_db(query):
    logger.debug('Querying REMOTE database')

    encoded = urllib.parse.quote(query.strip())
    req = urllib.request.Request('http://adage.cse.unsw.edu.au:8005/v1/graphs/sparql?query=' + encoded)
    req.add_header('Authorization', 'Basic ' + base64.b64encode(b'student:studentML').decode('utf-8'))
    data = urllib.request.urlopen(req).read().decode('utf-8')

    logger.debug('Retrieved from REMOTE database')

    data = json.loads(data)
    data = data['results']['bindings']

    return data

# Asks the external database using a given SPARQL query, and returns the result, mapping the values to a QueryResultSet.
def do_query(query):
    data = query_db(query)
    return QueryResultSet(data)

# Takes lists of the input RICs, topics, and dates, and converts it all into a SPARQL request.
def query(rics=[], topics=[], date_range=[]):
    r = get_ric_filter(rics)
    t = get_topic_filter(topics)
    d = get_date_filter(*date_range)
    q = QUERY_TEMPLATE.format(filter_ric=r, filter_topic=t, filter_daterange=d)
    return do_query(q)

# Gets a list of all RICs in the remote database.
def get_rics():
    return list(RICS_LIST)

# Gets a list of all topic codes in the remote database.
def get_topics():
    return list(TOPICS_LIST)

# Gets a list of all datetimes in the remote database.
def get_datetimes():
    return list(DATETIMES_LIST)

# Gets a list of all dates in the remote database.
def get_dates():
    return list(DATES_LIST)

_load_db_data()
