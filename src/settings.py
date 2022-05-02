from pytz import timezone
from datetime import datetime
from datetime import timedelta

# define formate for time strings
format = "%Y-%m-%d %H:%M:%S %Z%z"
# declare time zone
tz = timezone('US/Central')

# set the current date
date = (datetime.now() + timedelta(days=0))
# set current data as string
datefor = date.strftime('%Y-%m-%d')
