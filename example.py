from datetime import datetime
from seng.constants import DB_DATE_FORMAT
from seng.sparql import query
from seng.result import to_json
import json

def run():
    results = query(
        rics = ('BHP.AX', 'BLT.L'),
        topics = ('AMERS', 'COM'),
        daterange = (datetime.strptime('2015-10-01T00:00:00Z', DB_DATE_FORMAT), datetime.strptime('2015-10-10T00:00:00Z', DB_DATE_FORMAT))
    )

    results = sorted(results, key=lambda r: r.headline)
    jsonOutput = to_json(results)

    print(json.dumps(jsonOutput))

if __name__ == '__main__':
    run()
