from calendar_source import CalendarSourceTemplate

class Canvas(CalendarSourceTemplate):
    def stringify_event_name(self, event):
        partitioned_string = event['summary'].partition('[')
        return partitioned_string[0]
    
    def filter_event(self, event):
        return not 'calendar' in event['UID']

# example; https://canvas.illinois.edu/feeds/calendars/user_oy5oQZ5fExWwQr7GfvkKebDeZw17GJSB5U3WiQX7.ics