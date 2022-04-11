# Library Imports
from datetime import datetime
from datetime import timedelta
from xml.etree.ElementInclude import include
import requests
from icalendar import Calendar, Event, vDatetime
from pytz import timezone
import dateutil.rrule as rrule

import csv

from calendar_source_cbtf import Cbtf
from calendar_source_canvas import Canvas
"""
csvManage(calendars)

Takes a calendar link and lms name and writes to CSVs and makes new and old csv files
"""
def csvManage(calendar_link, lms):
    # list of new calendar links as dictionaries
    calendar_dictionaries = []
    # fieldnames for csvs
    fieldnames_ = ['name', 'type', 'course', 'start date', 'end date', 'start date and time', 'end date and time', 'end timestamp', 'source_name']
    # list of dictionaries
    new_data = []
    old_events = []

    # iterate through each link in list of links and add dictionaries for each calendar event in calendar_dictionaries
    if lms=="cbtf":
        cbtf_source = Cbtf(calendar_link)
        calendar_dictionaries.append(cbtf_source.request())
    if lms=="canvas":
        canvas_source = Canvas(calendar_link)
        calendar_dictionaries.append(canvas_source.request())

    # TODO: similar checks for moodle, pl, etc. go here

    # open total.csv for reading all old data
    # if file doesn't exist make new file w headers, close file, and reopen file for reading
    try:
        total_file = open('data/total.csv', 'r')
    except IOError:
        # TODO: open file as mode rw
        # TODO: this is breaking anyways, makes the value the key
        total_file = open('data/total.csv', 'w')
        csv_writer = csv.DictWriter(total_file, fieldnames=fieldnames_)
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
    csv_writer = csv.DictWriter(total_file, fieldnames=fieldnames_)
    new_writer = csv.DictWriter(new_file, fieldnames=fieldnames_)

    # write headers to new data file
    new_writer.writeheader()

    # write all new data to files
    for dic in new_data:
        csv_writer.writerow(dic)
        new_writer.writerow(dic)

    # close files
    total_file.close()
    new_file.close()
