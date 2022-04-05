from .template.calendar_source import CalendarSourceTemplate

class calendar(CalendarSourceTemplate):
    source_name = 'canvas'

    def extract_event_info(self, event, event_dictionary):
        partitioned_summary = event['summary'].partition('[')
        event_dictionary['name'] = partitioned_summary[0]

        event_dictionary['type'] = 'Needs to be manually sorted'

        partitioned_coursename = partitioned_summary[2].partition('_')
        event_dictionary['course'] = partitioned_coursename[0] + ' ' + partitioned_coursename[2].partition('_')[0]
        
    
    def filter_event(self, event):
        return not 'calendar' in event['UID']

    @staticmethod
    def matches_source(link):
        return 'canvas' in link


# example (liza's calendar); https://canvas.illinois.edu/feeds/calendars/user_oy5oQZ5fExWwQr7GfvkKebDeZw17GJSB5U3WiQX7.ics
