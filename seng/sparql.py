import base64
import json
import urllib.parse
import urllib.request

from datetime import datetime

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

QUERY_TEMPLATE = """
PREFIX w3: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fe: <http://adage.cse.unsw.edu.au/ontology/financial-events#>
PREFIX ins: <http://adage.cse.unsw.edu.au/resource/financial-events#>
PREFIX xs: <http://www.w3.org/2001/XMLSchema#>
SELECT ?s ?time ?headline ?newsBody
WHERE {{
?s w3:type fe:TRTHNewsEvent.
?s fe:relatedRIC ?ric.
?s fe:timeStamp ?t.
?t fe:startTime ?time.
?s fe:newsText ?newsBody.
?s fe:headLine ?headline.
?s fe:topicCode ?topicCode.
?s fe:languageOfNews "en".
 {filter_ric}
 {filter_topic}
 {filter_daterange}
}}
""".strip()


def get_ric_filter(rics):
    if len(rics) == 0:
        return ''
    each = map('?ric = ins:RIC_{}'.format, rics)
    cond = ' || '.join(each)
    return 'FILTER (%s)' % cond

def get_topic_filter(topics):
    if len(topics) == 0:
        return ''
    each = map('?topicCode = "N2:{}"'.format, topics)
    cond = ' || '.join(each)
    return 'FILTER (%s)' % cond

def get_date_filter(daterange):
    if len(daterange) == 0:
        return ''
    if len(daterange) != 2:
        raise ValueError('daterange length != 2')
    mapper = lambda d: '"{}"^^xs:dateTime'.format(d.strftime(DATE_FORMAT))
    cond_format = 'xs:dateTime(?time) > %s && xs:dateTime(?time) <= %s'
    cond = cond_format % tuple(map(mapper, daterange[:2]))
    return 'FILTER (%s)' % cond

def query(rics=[], topics=[], daterange=[]):
    r = get_ric_filter(rics)
    t = get_topic_filter(topics)
    d = get_date_filter(daterange)

    q = QUERY_TEMPLATE.format(filter_ric=r, filter_topic=t, filter_daterange=d)

    return do_query(q)

def do_query(query):
   encoded = urllib.parse.quote(query.strip())
   req = urllib.request.Request('http://adage.cse.unsw.edu.au:8005/v1/graphs/sparql?query=' + encoded)
   req.add_header('Authorization', 'Basic ' + base64.b64encode(b'student:studentML').decode('utf-8'))
   return json.load(urllib.request.urlopen(req))

print(query(
    rics = ('BHP.AX', 'BLT.L'),
    topics = ('AMERS', 'COM'),
    daterange = (datetime.strptime('2015-10-01T00:00:00Z', DATE_FORMAT), datetime.strptime('2015-10-10T00:00:00Z', DATE_FORMAT))
))
