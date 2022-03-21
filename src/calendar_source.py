from icalendar import Calendar
import requests
import settings
from settings import format, tz, date, datefor


class CalendarSourceTemplate:
    # intialize class using constructor
    def __init__(self, link, source_name):
        self.link = link
        self.source_name = source_name
    
    # main process for class, returns a string of events
    def request(self):
        # make request to the link and load downloaded file
        r = requests.get(self.link)
        # populate an ical object using text from downloaded file
        self.gcal = Calendar.from_ical(r.text)
        # each event in ical files start with "VEVENT"
        # so walk through ical file and parse an event at every instance of "VEVENT"
        events = self.gcal.walk('VEVENT')
        # parse each event to get its datatypes
        # if event does not have datatypes we should report, we filter them out
        events = filter(lambda event: any(self.get_event_data(event)), events)
        # we filter out any event that does should not be there according to our filter_event method
        events = filter(self.filter_event, events)
        # we transform each individual event to a dictionary using our generate_event_dictionary method
        events_dictionary = map(lambda event: self.generate_event_dictionary(event, *self.get_event_data(event)), events)
        # return our event dictionaries as a list
        return list(events_dictionary)
    
    # returns the start, end, and return rule for the event parameter
    def get_event_data(self, event):
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
    
    # generate the values for each of the keys of the event_dictionary
    def extract_event_info(self, event, event_dictionary):
        pass
    
    # return the event's information as a dicitonary
    def generate_event_dictionary(self, event, dtstart, dtend, nextrule):
        event_dictionary = {
            'name': '',
            'type': ''
        }
        # get event properties using extract_event_info helper method helper (for logic that varies class-to-class)
        self.extract_event_info(event, event_dictionary)
        # if repeating rule exists, report repeating rule date and end time after rule date
        if nextrule:
            length = (dtend - dtstart).total_seconds() / 60.0
            dtstart, dtend = nextrule, nextrule + length

        event_dictionary['timestamp'] = { 'start': dtstart, 'end': dtend }
        
        event_dictionary['source_name'] = self.source_name

        return event_dictionary

    # a filter helper function to exclude an non-desired calendar events
    def filter_event(self, event):
        return True

