from icalendar import Calendar
import requests
import settings
from settings import format, tz, date, datefor
import datetime
from dateutil.rrule import rrule

class CalendarSourceTemplate:
    # intialize class using constructor
    def __init__(self, link):
        self.link = link
    
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


        # just outputting the whole calender, for debugging
        f = open('output.ics', 'wb')
        f.write(self.gcal.to_ical())
        f.close()

        return list(events_dictionary)
    
    # returns the start, end, and return rule for the event parameter
    def get_event_data(self, event):
        # if a start date attribute exists for event, assign it to dtstart
        #   else set dtstart to false to show no start date
        if 'DTSTART' in event:
            if not isinstance(event['DTSTART'].dt, datetime.datetime):
                dtstart =  datetime.datetime.combine(event['DTSTART'].dt, datetime.datetime.min.time()).astimezone(tz)
            else:
                dtstart = event['DTSTART'].dt.astimezone(tz) # assign time in chosen timezone
        else:
            dtstart = False
        # if an end date attribute exists for event, assign it to dtend
        #   else set dtend to false to show no end date
        if 'DTEND' in event:
            if not isinstance(event['DTEND'].dt, datetime.datetime):
                dtend =  datetime.datetime.combine(event['DTEND'].dt, datetime.datetime.max.time()).astimezone(tz)
            else:
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
            'type': '',
            'course': ''
        }
        # get event properties using extract_event_info helper method helper (for logic that varies class-to-class)
        self.extract_event_info(event, event_dictionary)
        # if repeating rule exists, report repeating rule date and end time after rule date
        if nextrule:
            length = (dtend - dtstart).total_seconds() / 60.0
            dtstart, dtend = nextrule, nextrule + length

        # event_dictionary['timestamp'] = { 'start': dtstart, 'end': dtend }

        # format required; mm/dd/yyyy
        event_dictionary['start date'] = f'{dtstart.month}/{dtstart.day}/{dtstart.year}'     
        event_dictionary['end date'] = f'{dtend.month}/{dtend.day}/{dtend.year}'

        # format (arbitrarily decided): Time Day date. Month Year
        event_dictionary['start date and time'] = dtstart.strftime("%I:%M%p %A, %d. %B")
        event_dictionary['end date and time'] = dtstart.strftime("%I:%M%p %A, %d. %B")

        return event_dictionary

    # <------------- functions that will be overriden ------------->

    # exclude an non-desired calendar events
    def filter_event(self, event):
        return True
    
    # return the event's name using the string object
    def stringify_event_name(self, event):
        return ''

