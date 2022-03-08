from calendar_source import CalendarSourceTemplate

class Cbtf(CalendarSourceTemplate):
    def stringify_event_name(self, event):
        return event['summary'][6:]
    
    def filter_event(self, event):
        return not 'Exam' in event['summary']

if __name__ == '__main__':
    my_cbtf_source = Cbtf('https://cbtf.engr.illinois.edu/sched/icalendar/4f8ea873-ffbd-4cb1-8eb1-ebc0781a0898')
    print(my_cbtf_source.request())
