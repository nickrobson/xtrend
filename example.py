#!/usr/bin/env python

# example.py
# SENG3011 - Cool Bananas
#
# An example query that should get converted to SPARQL and comes back as an object.
# This is then output in a readable format (not the required JSON output).

from datetime import datetime
from seng.constants import DB_DATE_FORMAT
from seng.sparql import query
from seng.result import to_json
import json


def run():
    results = query(
        rics = ('BHP.AX', 'BLT.L'),
        topics = ('AMERS', 'COM'),
        date_range = (datetime.strptime('2015-10-01T00:00:00Z', DB_DATE_FORMAT), datetime.strptime('2015-10-10T00:00:00Z', DB_DATE_FORMAT))
    )

    results = sorted(results, key=lambda r: r.headline)
    json_output = to_json(results)

    print(json.dumps(json_output))


if __name__ == '__main__':
    run()
