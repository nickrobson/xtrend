# constants.py
# SENG3011 - Cool Bananas
#
# Constants used in other parts of the project.

import re

RELEASE_VERSION = '1.0.0'

DB_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
DATE_FORMAT = '%Y-%m-%d'

URI_PATTERN = re.compile(r'[0-9]{8}-[0-9]{9}-[A-Za-z0-9]{10}-[0-9]-[0-9]')

_RIC_PATTERN = r'(?:[A-Z0-9]+\.[A-Z]+)'
RIC_PATTERN = re.compile(_RIC_PATTERN)
RIC_LIST_PATTERN = re.compile(r'(?:'+_RIC_PATTERN+',)*'+_RIC_PATTERN)

_TOPIC_PATTERN = r'(?:[A-Z]{1,10})'
TOPIC_PATTERN = re.compile(_TOPIC_PATTERN)
TOPIC_LIST_PATTERN = re.compile(r'(?:'+_TOPIC_PATTERN+',)*'+_TOPIC_PATTERN)

QUERY_TEMPLATE = """
PREFIX w3: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fe: <http://adage.cse.unsw.edu.au/ontology/financial-events#>
PREFIX ins: <http://adage.cse.unsw.edu.au/resource/financial-events#>
PREFIX xs: <http://www.w3.org/2001/XMLSchema#>
SELECT ?s ?id ?ric ?topicCode ?lang ?time ?headline ?newsBody
WHERE {{
?s w3:type fe:TRTHNewsEvent.
?s fe:messageId ?id.
?s fe:relatedRIC ?ric.
?s fe:timeStamp ?t.
?t fe:startTime ?time.
?s fe:newsText ?newsBody.
?s fe:headLine ?headline.
?s fe:topicCode ?topicCode.
?s fe:languageOfNews ?lang.
?s fe:languageOfNews "en".
 {filter_ric}
 {filter_topic}
 {filter_daterange}
}}
""".strip()

LIST_RICS_QUERY = """
PREFIX w3: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fe: <http://adage.cse.unsw.edu.au/ontology/financial-events#>
SELECT DISTINCT ?ric
WHERE {{
?s w3:type fe:TRTHNewsEvent.
?s fe:relatedRIC ?ric.
?s fe:languageOfNews "en".
}}
""".strip()

LIST_TOPICS_QUERY = """
PREFIX w3: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fe: <http://adage.cse.unsw.edu.au/ontology/financial-events#>
SELECT DISTINCT ?topicCode
WHERE {{
?s w3:type fe:TRTHNewsEvent.
?s fe:topicCode ?topicCode.
?s fe:languageOfNews "en".
}}
""".strip()

LIST_DATES_QUERY = """
PREFIX w3: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fe: <http://adage.cse.unsw.edu.au/ontology/financial-events#>
SELECT DISTINCT ?time
WHERE {{
?s w3:type fe:TRTHNewsEvent.
?s fe:timeStamp ?t.
?t fe:startTime ?time.
?s fe:languageOfNews "en".
}}
""".strip()
