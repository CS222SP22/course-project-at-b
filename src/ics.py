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
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pl_scraping import getClassLinks

filename = 'data/ical_links.json'

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
	# if lms is prairielearn, get links first
	if lms=="prairielearn":
		driver = webdriver.Chrome(ChromeDriverManager().install())
		pl_links = getClassLinks(open("data/secret.txt", "r"), driver)
		for link in pl_links:
			data['links'].append({'url':link, 'lms': lms})
			data['link-count'] += 1
	else:
		data['links'].append({'url':link, 'lms': lms})
		data['link-count'] += 1
	
	# writing back to json file
	with open(filename, 'w') as f:
		json.dump(data, f)
	
	print('Added Link(s) to Source File')

def read(): 
	try:
		ofs = open(filename, 'r')
	except IOError:
		create_file()
		print('Unable to find file, creating it!')
	else:
		data = json.load(ofs)

		# iterate through links and generate event strings
		new_csv = True
		for d in data['links']:
			ics_reader.csvManage(d['url'], d['lms'], new_csv)
			new_csv = False

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
	
