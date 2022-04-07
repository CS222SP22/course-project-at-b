import json
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

# if __name__ == '__main__':
#     my_cbtf_source = Cbtf('https://cbtf.engr.illinois.edu/sched/icalendar/db3b45d1-f730-4992-8842-a08401b99b32')
#     print(json.dumps(my_cbtf_source.request(), indent=4, default=str))
