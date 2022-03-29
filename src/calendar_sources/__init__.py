import os

__all__ = []

# import all class templates files and store them in __all__
for module in os.listdir(os.path.dirname(__file__)):
    # skip files that are not class templates
    if module == '__init__.py' or module == 'calendar_source.py' or module[-3:] != '.py':
        continue
    __all__.append(__import__(f'calendar_sources.{module[:-3]}', globals(), locals(), ['calendar']))
