from datetime import datetime
from seng.constants import DB_DATE_FORMAT
from seng.sparql import query

results = query(
    rics = ('BHP.AX', 'BLT.L'),
    topics = ('AMERS', 'COM'),
    daterange = (datetime.strptime('2015-10-01T00:00:00Z', DB_DATE_FORMAT), datetime.strptime('2015-10-10T00:00:00Z', DB_DATE_FORMAT))
)

for result in results:
    print(result)
