'''ics.py

Usage:
    ics.py add <link>
    ics.py read
    ics.py (-h | --help)

Options:
    -h --help       Show this screen.
    --version       Show version.
'''
from docopt import docopt
import sys
import ics_reader

from notion import send_to_notion

filename = 'ical_links.txt'

def add(link):
    file1 = open(filename, 'a')
    file1.writelines(link)
    file1.close()
    print("Added Link to Source File")

def read(): 
    try:
        ofs = open(filename, 'r')
    except IOError:
        print ("Could not open %s, please create file!" % filename)
    else:
        read_lines = ofs.readlines()
        event_strings = ics_reader.readICal(read_lines)
        for line in event_strings:
            # print(line + '\n')
            # print(line)
            send_to_notion(line)

def main(arguments):
    if arguments['add']:
        add(arguments['<link>'])
    elif arguments['read']:
        read()

if __name__ == '__main__':
    arguments = docopt(__doc__, version='ics.py 1.0')
    main(arguments)
    
