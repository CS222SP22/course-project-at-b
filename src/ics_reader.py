# Library Imports
from datetime import datetime
from datetime import timedelta
import requests
from icalendar import Calendar, Event, vDatetime
from pytz import timezone
import dateutil.rrule as rrule

import calendar_source_cbtf
import calendar_source_canvas

"""
ReadICal(calendars)

Takes a list of calendar links and returns a list of strings 
Each string in the list contains the summary/title, start date, and end date of each event
"""
def readICal(calendars):

    event_strings = []

    # iterate through each link in list of links
    for calendar_link in calendars:
        calendar_sources = []

        if "cbtf" in calendar_link:
            cbtf_source = calendar_source_cbtf.Cbtf(calendar_link)
            calendar_sources.append(cbtf_source)
        if "canvas" in calendar_link:
            canvas_source = calendar_source_canvas.Canvas(calendar_link)
            calendar_sources.append(canvas_source)
        
        # TODO: similar checks for moodle needed

        for cal_src in calendar_sources:
            event_strings.append(cal_src.request())
    
    # return list of events as string
    return event_strings
            