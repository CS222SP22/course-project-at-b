'''ics.py

Usage:
    ics.py add <link> <lms>
    ics.py read
    ics.py (-h | --help)

Options:
    -h --help       Show this screen.
    --version       Show version.
'''
from docopt import docopt
import sys
import ics_reader
import json

filename = 'ical_links.json'

def add(link, lms):
	with open(filename, 'r') as f:
		data = json.load(f)
	
	#iterate through existing vals to ensure that it doesn't already exist - update if so
	for d in data['links']:
		if d['url'] == link or d['lms'] == lms:
			print('Value already exists, updating')
			d['url'] = link
			d['lms'] = lms
			
			# writing back to json file
			with open(filename, 'w') as f:
				json.dump(data, f)
			return

	# value doesn't already exist, hence adding to list of LMSes
	data['links'].append({'url':link, 'lms': lms})
	data['link-count'] += 1
	
	# writing back to json file
	with open(filename, 'w') as f:
		json.dump(data, f)
	
	print('Added Link to Source File')

def read():
    try:
        ofs = open(filename, 'r')
    except IOError:
        create_file()
        print('Unable to find file, creating it!')
    else:
        data = json.load(ofs)
        # iterate through links and generate event strings
        for d in data['links']:
            #TODO: Pass in the LMS, for the purpose of better filtering.
            print(d)
            event_strings = ics_reader.readICal(d['url'], d['lms'])
            for line in event_strings:
                print(line + '\n')

def create_file():
    data = {'link-count':0, 'links':[]}
    with open(filename, 'w+') as f:
        json.dump(data, f)

def main(arguments):
    if arguments['add']:
        add(arguments['<link>'], arguments['<lms>'])
    elif arguments['read']:
        read()

if __name__ == '__main__':
    arguments = docopt(__doc__, version='ics.py 1.0')
    main(arguments)
    
