
import datetime as dt
date: dt.date = "23.02.2019"
date2: dt.date = None

date = dt.datetime.strptime(date, '%d.%m.%Y').date()

date2 = dt.datetime.now().date()

print(date, date2)