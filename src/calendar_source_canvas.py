from calendar_source import CalendarSourceTemplate

class Canvas(CalendarSourceTemplate):
    def extract_event_info(self, event, event_dictionary):
        partitioned_string = event['summary'].partition('[')
        event_dictionary['name'] = partitioned_string[0]

        event_dictionary['type'] = 'Needs to be manually sorted'
    
    def filter_event(self, event):
        return not 'calendar' in event['UID']

# example; https://canvas.illinois.edu/feeds/calendars/user_oy5oQZ5fExWwQr7GfvkKebDeZw17GJSB5U3WiQX7.ics