# Library Imports
from datetime import datetime
from datetime import timedelta
from xml.etree.ElementInclude import include
import requests
from icalendar import Calendar, Event, vDatetime
from pytz import timezone
import dateutil.rrule as rrule

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import csv
import notion
import json

import calendar_sources

"""
csvManage(calendars)
Takes a calendar link and lms name and writes to CSVs and makes new and old csv files
"""
def csvManage(calendar_links, output_option):   # CHANGE THIS SHOULD ONLY BE CALLED ONCE

    # # clearing new_data TODO:maybe not needed?
    # with open("data/new_data.csv", 'r+') as f:
    #     f.truncate(0)
        
    # fieldnames for csvs
    fieldnames_default_ = ['name', 'type', 'course', 'start date', 'end date', 'start date and time', 'end date and time', 'end timestamp', 'source_name']
    fieldnames_todoist_ = ['TYPE','CONTENT', 'DESCRIPTION', 'DATE','DATE_LANG']

    # iterate through each link in list of links
    calendar_dictionaries = []  # list of new calendar links as dictionaries
    for calendar_link in calendar_links:
        calendar_source_classes = []

        for calendar_source in calendar_sources.__all__:
            if calendar_source.calendar.matches_source(calendar_link['url']):
                calendar_source_classes.append(calendar_source.calendar(calendar_link['url']))
                break

        for cal_src in calendar_source_classes:
            calendar_dictionaries.append(cal_src.request())
    # list of dictionaries
    new_data = []
    old_events = []

    # open total.csv for reading all old data
    # if file doesn't exist make new file w headers, close file, and reopen file for reading
    try:
        total_file = open('data/total.csv', 'r')
    except IOError:
        # TODO: open file as mode rw
        # TODO: this is breaking when re-writing files, makes the value the key
        total_file = open('data/total.csv', 'w')
        csv_writer = csv.DictWriter(total_file, fieldnames=fieldnames_default_)
        csv_writer.writeheader()
        total_file.close()
        total_file = open('data/total.csv', 'r')

    # convert all data in csv DictReader object into a list and close reading file
    csv_reader = csv.DictReader(total_file)
    for dic in csv_reader:
        old_events.append(dic)
    total_file.close()

    # check if each new event exists in the old data and add it to new_data if not found
    for dictionary in calendar_dictionaries:
        for event_dic in dictionary:
            # print(event_dic)
            found = False
            for old_dic in old_events:
                if event_dic["name"].strip() == old_dic["name"].strip():
                    found = True
            if not found:
                new_data.append(event_dic)

    # updated total data file:
    total_file = open('data/total.csv', mode='a')
    total_writer = csv.DictWriter(total_file, fieldnames=fieldnames_default_)
    total_writer.writerows(new_data)
    total_file.close()
    
    # update new data file, format dependent on user's output option
    if output_option=='notion':
        try:
            ofs = open('data/notion_config.json', 'r')
        except IOError:
            print('You must configure notion first')
        else:
            print(new_data)
            data = json.load(ofs)
            notion.send_to_notion(new_data, data['database_id'], data['api_key'])
    elif output_option=='todoist':
        convertToTodoistFormat(new_data)

def convertToTodoistFormat(notion_new_data):    #TODO: make this just take and return a list of dicts
    todoist_field_names = ['TYPE','CONTENT', 'DESCRIPTION', 'DATE','DATE_LANG']
    todoist_new_file = open('data/new_data.csv', mode = 'w')          
    todoist_writer = csv.DictWriter(todoist_new_file, fieldnames=todoist_field_names)

    todoist_writer.writeheader()

    # convert notion's format to todoist format, following these guidelines; https://todoist.com/help/articles/how-to-format-your-csv-file-so-you-can-import-it-into-todoist
    for old_format_dict in notion_new_data:

        # todoist doesn’t support start dates, so i’m adding it to the description instead
        # lmao turns out this doesn't even matter
        description = old_format_dict['course']
        if old_format_dict['start date and time']!= old_format_dict['end date and time']:
            description += f', Start date: {old_format_dict["start date and time"]}'
        description += f', Task Source LMS: {old_format_dict["source_name"]}'

        new_format_dict = {
            'TYPE': 'task', #different for quizzes? (after we fix sorting in canvas)
            'CONTENT': old_format_dict['name'],            
            'DESCRIPTION': description,
            'DATE': old_format_dict['end date'], 
            'DATE_LANG': 'en'
        }
        todoist_writer.writerow(new_format_dict)

    todoist_new_file.close()
