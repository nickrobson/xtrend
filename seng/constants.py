# constants.py
# SENG3011 - Cool Bananas
#
# Constants used in other parts of the project.

DB_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

QUERY_TEMPLATE = """
PREFIX w3: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fe: <http://adage.cse.unsw.edu.au/ontology/financial-events#>
PREFIX ins: <http://adage.cse.unsw.edu.au/resource/financial-events#>
PREFIX xs: <http://www.w3.org/2001/XMLSchema#>
SELECT ?s ?ric ?topicCode ?time ?headline ?newsBody
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
