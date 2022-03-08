# Library Imports
from datetime import datetime
from datetime import timedelta
import requests
from icalendar import Calendar, Event, vDatetime
from pytz import timezone
import dateutil.rrule as rrule

"""
GetEventData(event, date, tz)

Takes the event input and returns the desired atributes of that event
    - Start Date (dtstart)
    - End Date (dtend)
    - Next Time event occurs if a repeating rule exists (nextrule)
"""
def getEventData(event, date, tz):
    # if a start date attribute exists for event, assign it to dtstart
    #   else set dtstart to false to show no start date
    if 'DTSTART' in event:
        dtstart = event['DTSTART'].dt.astimezone(tz) # assign time in chosen timezone
    else:
        dtstart = False
    # if an end date attribute exists for event, assign it to dtend
    #   else set dtend to false to show no end date
    if 'DTEND' in event:
        dtend = event['DTEND'].dt.astimezone(tz) # assign time in chosen timezone
    else:
        dtend = False
    # if a repeating rule exists, calculate the next time the rule exists after today
    #   and assign it to next rule
    #   else set nextrule to false to show no repeating rule
    if 'RRULE' in event:
        ruletext = event['RRULE'].to_ical().decode()
        rule = rrule.rrulestr(ruletext, dtstart=event['DTSTART'].dt)
        nextrule=rule.after(date.astimezone(tz)) # assign time in chosen timezone
    else:
        nextrule = False
    
    # return the dates data for the event
    return dtstart, dtend, nextrule

"""
EventToString(event, date, tz)

Takes the event input and returns the event as a string version
String has the summary title of the event along with start and end times
"""
def eventToString(event, date, tz):
    # create empty return value string
    event_string = ""

    # obtain event data using GetEventData()
    dtstart, dtend, nextrule = getEventData(event, date, tz)

    # if event does not have datatypes we should report, we return empty
    if not (dtstart or dtend or nextrule):
        return ""

    # add summary/title of the event to return string
    event_string += str(event['summary']).strip()

    # if repeating rule does not exist, report start and end dates
    #   else report repeating rule date and end time after rule date
    if not nextrule:
            event_string += ("\n%s to %s" % (dtstart, dtend))
    else:
        length = (dtend - dtstart).total_seconds() / 60.0
        event_string += ("\n%s to %s" % (nextrule, nextrule + length))

    # return event as developed string
    return event_string

"""
ReadICal(link)

Takes a link and returns a list of strings 
Each string in the list contains the summary/title, start date, and end date of each event
"""
def readICal(link):
    # create empty return value list
    event_strings = []
    # define formate for time strings
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    # declare time zone
    tz = timezone('US/Central')

    # set the current date
    date = (datetime.now() + timedelta(days=0))
    # set current data as string
    datefor = date.strftime('%Y-%m-%d')

    # make request to the link and load downloaded file
    r = requests.get(link)
    # populate an ical object using text from downloaded file
    gcal = Calendar.from_ical(r.text)

    # each event in ical files start with "VEVENT"
    # so walk through ical file and stop at every instance of "VEVENT"
    for event in gcal.walk('VEVENT'):
        event_strings.append(eventToString(event, date, tz))
    
    # return list of events as string
    return event_strings
            
