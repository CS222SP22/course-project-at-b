import json
from calendar_source import CalendarSourceTemplate

class Moodle(CalendarSourceTemplate):
    def extract_event_info(self, event, event_dictionary):
        event_dictionary['source_name'] = "moodle"

        event_dictionary['name'] = event['summary'][6:]

        event_dictionary['type'] = 'Exam/Quiz'

        partitioned_summary = event['summary'][6:].partition(" ")	
        event_dictionary['course'] = partitioned_summary[0] + " " + partitioned_summary[2].partition(" ")[0]
    
    def filter_event(self, event):
        return not 'Exam' in event['summary']

if __name__ == '__main__':
    my_moodle_source = Moodle('https://learn.illinois.edu/calendar/export_execute.php?userid=537403&authtoken=d30326f98ee928652597c810df4a268a7b531b84&preset_what=all&preset_time=custom')
    print(json.dumps(my_moodle_source.request(), indent=4, default=str))
