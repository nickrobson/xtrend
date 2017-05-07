#!/usr/bin/env python3

# example2.py
# SENG3011 - Cool Bananas
#
# An example query for the second API that should get converted

from datetime import datetime, date
from seng.core.constants import DB_DATE_FORMAT
import urllib.request
import json, sys

stingray_url = 'http://ec2-54-160-211-66.compute-1.amazonaws.com:3000/api/company_returns?'

# Converts the submitted RIC string into the format required for the SPARQL.
def get_ric_filter(rics):
    s = 'InstrumentID='
    for r in rics:
        s += r
        s += ','
    s = s[:-1]
    return s

# Converts the submitted vars into the format required for the SPARQL.
def get_var_filter(var):
    s = 'ListOfVar='
    for v in var:
        s += v
        s += ','
    s = s[:-1]
    return s


# Converts the submitted date into the format required for the SPARQL.
def get_date_filter(d):
    s = 'DateOfInterest='
    s += str(d.day)
    s += '%2F'
    s += str(d.month)
    s += '%2F'
    s += str(d.year)
    return s

# Does the query.
def do_query(query):
    print(query)
    return urllib.request.urlopen(query).read().decode('utf-8')

# Converts the arguments into the proper SPARQL command, then does it.
def query(rics=[], var=[], upper_window=0, lower_window=0, date_of_interest=date(1970, 1, 1)):
    r = get_ric_filter(rics)
    v = get_var_filter(var)
    u = 'UpperWindow=' + str(upper_window)
    l = 'LowerWindow=' + str(lower_window)
    d = get_date_filter(date_of_interest)
    return do_query(stingray_url + r + '&' + v + '&' + u + '&' + l + '&' + d)

def run():
    results = query(
        rics = ('ABP.AX',),
        var = ('AV_Return',),
        upper_window = 5,
        lower_window = 3,
        date_of_interest = date(2012, 12, 10)
    )

    data = json.loads(results)

    print(json.dumps(data, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    run()
