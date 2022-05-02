import json
import importlib
import calendar_sources

for i in calendar_sources.__all__:
    print(i.calendar.source_name)
