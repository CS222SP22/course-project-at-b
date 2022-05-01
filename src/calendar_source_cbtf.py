from calendar_source import CalendarSourceTemplate

class Cbtf(CalendarSourceTemplate):
    def extract_event_info(self, event, event_dictionary):
        event_dictionary['source_name'] = "cbtf"

        event_dictionary['name'] = event['summary'][6:]

        event_dictionary['type'] = 'Exam/Quiz'

        partitioned_summary = event['summary'][6:].partition(" ")	
        event_dictionary['course'] = partitioned_summary[0] + " " + partitioned_summary[2].partition(" ")[0]
    
    def filter_event(self, event):
        return not 'Exam' in event['summary']

