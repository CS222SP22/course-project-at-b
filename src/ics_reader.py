from datetime import datetime
from datetime import timedelta

import requests
from icalendar import Calendar, Event, vDatetime
from pytz import timezone
import dateutil.rrule as rrule

format = "%Y-%m-%d %H:%M:%S %Z%z"

tz = timezone('US/Central')

file1 = open('lines.txt', 'r')
calendars = file1.readlines()

date = (datetime.now() + timedelta(days=0))
datefor = "%s" % date.strftime('%Y-%m-%d')

for calendar in calendars:
    r = requests.get(calendar)
    gcal = Calendar.from_ical(r.text)

    for event in gcal.walk('VEVENT'):
        if 'DTSTART' in event:
            try:
                dtstart = event['DTSTART'].dt.astimezone(tz)
            except:
                dtstart = False
        if 'DTEND' in event:
            try:
                dtend = event['DTEND'].dt.astimezone(tz)
            except:
                dtend = False
        if 'RRULE' in event:
            try:
                ruletext = event['RRULE'].to_ical().decode()
                rule = rrule.rrulestr(ruletext, dtstart=event['DTSTART'].dt)
                nextrule=rule.after(date.astimezone(tz))
            except:
                nextrule = False
        else:
            nextrule = False

        if dtstart or dtend or nextrule:
            if datefor in "%s" % dtstart or datefor in "%s" % dtend or datefor in "%s" % nextrule:
                print("\n", event['summary'])

                if dtstart and dtend:
                    lenght = (dtend - dtstart).total_seconds()/60
                else:
                    lenght = False

                if not nextrule:
                    if lenght:
                        print("start: %s for %s minutes" % (dtstart, lenght))
                else:
                    print("start: %s for %s minutes" % (nextrule, lenght))