# Library Imports
from datetime import datetime
from datetime import timedelta
from xml.etree.ElementInclude import include
import requests
from icalendar import Calendar, Event, vDatetime
from pytz import timezone
import dateutil.rrule as rrule

import csv

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

"""
csvManage(calendars)

Takes a list of calendar links and writes to CSVs and makes new and old csv files
"""
def csvManage(calendars):
    # list of new calendar links as dictionaries
    calendar_dictionaries = []
    # fieldnames for csvs
    fieldnames = ['name', 'type', 'course', 'timestamp','source_name']
    # list of dictionaries
    new_data = []
    old_events = []

    # iterate through each link in list of links and add dictionaries for each calendar event in calendar_dictionaries
    for calendar_link in calendars:
        if "cbtf" in calendar_link:
            cbtf_source = calendar_source_cbtf.Cbtf(calendar_link)
            calendar_dictionaries.append(cbtf_source.request())
        if "canvas" in calendar_link:
            canvas_source = calendar_source_canvas.Canvas(calendar_link)
            calendar_dictionaries.append(canvas_source.request())

    # open total.csv for reading all old data
    # if file doesn't exist make new file w headers, close file, and reopen file for reading
    try:
        total_file = open('data/total.csv', 'r')
    except IOError:
        # TODO: open file as mode rw
        total_file = open('data/total.csv', 'w')
        csv_writer = csv.DictWriter(total_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        total_file.close()
        total_file = open('data/total.csv', 'r')

    # convert all data in csv DictReader object into a list and close reading file
    csv_reader = csv.DictReader(total_file)
    for dic in csv_reader:
        old_events.append(dic)
    total_file.close()

    # check if each new event exists in the old data and add it to new_data if not found
    for event_dic in calendar_dictionaries[0]:
        found = False
        for old_dic in old_events:
            if event_dic["name"].strip() == old_dic["name"].strip():
                found = True
        if not found:
            new_data.append(event_dic)    
    
    # open files for writing or appending and initialize DictWriter objects
    total_file = open('data/total.csv', mode='a')
    new_file = open('data/new_data.csv', mode='w')
    csv_writer = csv.DictWriter(total_file, fieldnames=fieldnames)
    new_writer = csv.DictWriter(new_file, fieldnames=fieldnames)

    # write headers to new data file
    new_writer.writeheader()

    # write all new data to files
    for dic in new_data:
        csv_writer.writerow(dic)
        new_writer.writerow(dic)

    # close files
    total_file.close()
    new_file.close()
