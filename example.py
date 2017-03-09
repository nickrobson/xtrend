from datetime import datetime
from seng.constants import DB_DATE_FORMAT
from seng.sparql import query
import json

def run():
    results = query(
        rics = ('BHP.AX', 'BLT.L'),
        topics = ('AMERS', 'COM'),
        daterange = (datetime.strptime('2015-10-01T00:00:00Z', DB_DATE_FORMAT), datetime.strptime('2015-10-10T00:00:00Z', DB_DATE_FORMAT))
    )

    results = sorted(results, key=lambda r: r.headline)

    jsonOutput = {}
    jsonOutput["NewsDataSet"] = list(map(changeFormat, results))

    print(json.dumps(jsonOutput))

def changeFormat(result):
    currResult = {}
    currResult["InstrumentID"] = ""
    currResult['TimeStamp'] = str(result.time)
    currResult["Headline"] = result.headline
    currResult["NewsText"] = result.news_body
    
    return currResult

if __name__ == '__main__':
    run()
