#!/usr/bin/env python3

# example.py
# SENG3011 - Cool Bananas
#
# An example query that should get converted to SPARQL and comes back as an object.
# This is then output in a readable format (not the required JSON output).

from datetime import datetime
from seng.core.constants import DB_DATE_FORMAT
from seng.core.sparql import query
import json


def run():
    results = query(
        rics = ('BHP.AX', 'BLT.L'),
        topics = ('AMERS', 'COM'),
        date_range = (datetime.strptime('2015-10-01T00:00:00Z', DB_DATE_FORMAT), datetime.strptime('2015-10-10T00:00:00Z', DB_DATE_FORMAT))
    )

    json_output = results.to_json()

    print(json.dumps(json_output, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    run()
