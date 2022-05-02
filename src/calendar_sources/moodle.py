from .template.calendar_source import CalendarSourceTemplate

class calendar(CalendarSourceTemplate):
    source_name = "moodle"

    def extract_event_info(self, event, event_dictionary):
        event_dictionary['source_name'] = "moodle"

        event_dictionary['name'] = event['summary']

        event_dictionary['type'] = 'Needs to be manually sorted'

        category_data = event.get('categories').to_ical().decode()
        res = [i for i in range(len(category_data)) if category_data.startswith(" ", i)]
        event_dictionary['course'] = category_data[:res[1]]
    
    def filter_event(self, event):
        return 'categories' in event

    @staticmethod
    def matches_source(link):
        return 'learn.illinois' in link