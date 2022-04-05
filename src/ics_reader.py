# Library Imports
from datetime import datetime
from datetime import timedelta
from xml.etree.ElementInclude import include
import requests
from icalendar import Calendar, Event, vDatetime
from pytz import timezone
import dateutil.rrule as rrule

import calendar_sources

"""
ReadICal(calendars)

Takes a list of calendar links and returns a list of strings 
Each string in the list contains the summary/title, start date, and end date of each event
"""
def readICal(calendars):

    event_strings = []

    # iterate through each link in list of links
    for calendar_link in calendars:
        calendar_source_classes = []

        for calendar_source in calendar_sources.__all__:
            if calendar_source.calendar.matches_source(calendar_link):
                calendar_source_classes.append(calendar_source.calendar(calendar_link))
                break

        for cal_src in calendar_source_classes:
            # print(cal_src.link)
            event_strings.append(cal_src.request())
    
    # return list of events as string
    return event_strings