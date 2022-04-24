'''ics.py

Usage:
	ics.py add <link> <lms>
	ics.py read [notion | todoist]
	ics.py (-h | --help)

Options:
	-h --help       Show this screen.
	--version       Show version.
'''
from docopt import docopt
import sys
import ics_reader
import json

filename = 'data/user_input.json'

def add(link, lms):
	lms = lms.lower()
	try:
		open(filename, 'r').close()
	except IOError:
		create_file()
		print('Unable to find file, creating it!')
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

def read(output_option): 
	try:
		ofs = open(filename, 'r')
	except IOError:
		create_file()
		print('Unable to find file, creating it!')
	else:
		data = json.load(ofs)
		
		# iterate through links and generate event strings
		ics_reader.csvManage(data['links'], output_option)

def create_file():
	data = {'link-count':0, 'links':[]}
	with open(filename, 'w+') as f:
		json.dump(data, f)

def main(arguments):
	if arguments['add']:
		add(arguments['<link>'], arguments['<lms>'])
	elif arguments['read']:
		output_option = 'todoist' if arguments['todoist'] else 'notion'
		read(output_option)

if __name__ == '__main__':
	arguments = docopt(__doc__, version='ics.py 1.0')
	main(arguments)
	
