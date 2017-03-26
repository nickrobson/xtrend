# constants.py
# SENG3011 - Cool Bananas
#
# Constants used in other parts of the project.

import re

RELEASE_VERSION = '1.0.0'

DB_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

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

_RIC_PATTERN = r'(?:\.[A-Z0-9]+|[A-Z0-9]+(?:\.[A-Z]+)?)'
RIC_PATTERN = re.compile(_RIC_PATTERN)
RIC_LIST_PATTERN = re.compile(r'(?:'+_RIC_PATTERN+',)*'+_RIC_PATTERN)
