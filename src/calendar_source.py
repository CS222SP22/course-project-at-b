from icalendar import Calendar
import requests
import settings
from settings import format, tz, date, datefor


class CalendarSourceTemplate:
    # intialize class using constructor
    def __init__(self, link):
        self.link = link
    
    # main process for class, returns a string of events
    def request(self):
        # create empty return value list
        events_string = []
        # make request to the link and load downloaded file
        r = requests.get(self.link)
        # populate an ical object using text from downloaded file
        self.gcal = Calendar.from_ical(r.text)
        # each event in ical files start with "VEVENT"
        # so walk through ical file and parse an event at every instance of "VEVENT"
        events = map(lambda event: event, self.gcal.walk('VEVENT'))
        # parse each event to get its datatypes
        # if event does not have datatypes we should report, we filter them out
        events = filter(lambda event: any(self.get_event_data(event)), events)
        # we filter out any event that does should not be there according to our filter_event method
        events = filter(self.filter_event, events)
        # we transform each individual event to a string using our stringify method
        events_string = map(lambda event: self.stringify_event(event, *self.get_event_data(event)), events)
        # return our event strings as a list
        return list(events_string)
    
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
    
    # return the event's name using the string object
    def stringify_event_name(self, event):
        return ''
    
    # return the event's name and the time using stringify_event_name as a helper function
    def stringify_event(self, event, dtstart, dtend, nextrule):
        event_name = self.stringify_event_name(event)
        # if repeating rule does not exist, report start and end dates
        # else report repeating rule date and end time after rule date
        if not nextrule:
            event_timestamp = ("%s to %s" % (dtstart, dtend))
        else:
            length = (dtend - dtstart).total_seconds() / 60.0
            event_timestamp = ("%s to %s" % (nextrule, nextrule + length))

        return event_name + ': ' + event_timestamp

    # a filter helper function to exclude an non-desired calendar events
    def filter_event(self, event):
        return True

