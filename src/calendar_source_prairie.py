from calendar_source import CalendarSourceTemplate

class Prairie(CalendarSourceTemplate):
    def extract_event_info(self, event, event_dictionary):
        event_dictionary['source_name'] = "prairielearn"

        event_dictionary['name'] = "TBD"

        event_dictionary['type'] = 'Needs to be manually sorted'

        event_dictionary['course'] = "TBD"
    
    def filter_event(self, event):
        return True