# Library Imports
from datetime import datetime
from datetime import timedelta
from xml.etree.ElementInclude import include
import requests
from icalendar import Calendar, Event, vDatetime
from pytz import timezone
import dateutil.rrule as rrule

from calendar_source_cbtf import Cbtf
from calendar_source_canvas import Canvas

"""
ReadICal(link)

Takes a link and returns a list of strings 
Each string in the list contains the summary/title, start date, and end date of each event
"""

def readICal(link, lms):
    # create empty return value list
    event_strings = []
    calendar_sources = []

    if lms == "cbtf":
        cbtf_source = Cbtf(link)
        calendar_sources.append(cbtf_source)

    if lms =="canvas":
        canvas_source = Canvas(link)
        calendar_sources.append(canvas_source)

    # TODO: similar checks for moodle needed

    for cal_src in calendar_sources:
        event_strings.append(cal_src.request())

    print(len(event_strings))
    # return list of events as string
    return event_strings
