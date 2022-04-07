import json
from calendar_source import CalendarSourceTemplate

class Moodle(CalendarSourceTemplate):
    def extract_event_info(self, event, event_dictionary):
        event_dictionary['source_name'] = "moodle"

        event_dictionary['name'] = event['summary']

        event_dictionary['type'] = 'Needs to be manually sorted'

        category_data = event.get('categories').to_ical().decode()
        res = [i for i in range(len(category_data)) if category_data.startswith(" ", i)]
        event_dictionary['course'] = category_data[:res[1]]
    
    def filter_event(self, event):
        return 'categories' in event

# if __name__ == '__main__':
#     my_moodle_source = Moodle('https://learn.illinois.edu/calendar/export_execute.php?userid=545202&authtoken=88cb7b03f8f6317d5d16e8096a3eed8232773bb7&preset_what=all&preset_time=recentupcoming')
#     print(json.dumps(my_moodle_source.request(), indent=4, default=str))
