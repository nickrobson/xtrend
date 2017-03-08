from datetime import datetime
from seng.constants import DB_DATE_FORMAT
from seng.sparql import query

def run():
    results = query(
        rics = ('BHP.AX', 'BLT.L'),
        topics = ('AMERS', 'COM'),
        daterange = (datetime.strptime('2015-10-01T00:00:00Z', DB_DATE_FORMAT), datetime.strptime('2015-10-10T00:00:00Z', DB_DATE_FORMAT))
    )

    results = sorted(results, key=lambda r: r.headline)

    for i, result in enumerate(results):
        print('\n\n\nHeadline:', result.headline)
        print('Time:', result.time)
        print('RIC:', result.ric)
        print('Topic Code:', result.topic_code)
        print('Article:', result.news_body)
        if i != len(results) - 1:
            input('Press [ENTER] to see the next article.')

if __name__ == '__main__':
    run()
