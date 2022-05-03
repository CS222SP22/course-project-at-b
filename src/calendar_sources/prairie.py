from .template.calendar_source import CalendarSourceTemplate

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from datetime import datetime, date

class calendar(CalendarSourceTemplate):
    source_name = 'prairielearn'

    def extract_event_info(self, event, event_dictionary):

        event_dictionary['source_name'] = "prairielearn"

        event_dictionary['name'] = "TBD"

        event_dictionary['type'] = 'Needs to be manually sorted'

        event_dictionary['course'] = "TBD"
    
    def filter_event(self, assign):
        return "instance #" in assign[2] or assign[2] == "None" or "Assessment closed" in assign[2]
    
    def request(self):
        # Login to PL
        f = open("data/secret.txt", "r")
        email = f.readline()    
        password = f.readline()    
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://www.prairielearn.org/")
        driver.find_element(By.LINK_TEXT, "Log in").click()
        time.sleep(2) 
        driver.find_element(By.LINK_TEXT, "Sign in with Illinois").click()
        time.sleep(2) 
        driver.find_element(By.ID, "userNameInput").send_keys(email + Keys.ENTER)
        time.sleep(2) 
        driver.find_element(By.ID, "passwordInput").send_keys(password + Keys.ENTER)
        time.sleep(2) 
    
        driver.get(self.link)
        
        # Webscrape PL
        # client = ScrapingAntClient(token='2b6ffb675d654a998e1d64e08953bdac')
        # page_source = client.general_request(self.link).content
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        spans = soup.find_all('span', {'class' : 'navbar-text'})
        this_class = [span.get_text() for span in spans]

        assignments = []
        # get data on page
        for assignment in soup.find_all(['tr']):
            assign = []
            for attr in assignment.find_all(['td']):
                assign.append(attr.get_text().strip())
            if len(assign) > 0:
                assignments.append(assign[:len(assign)-1])
    
        assignments_list = []

        for assign in assignments:
            if self.filter_event(assign):
                continue

            time_str = assign[2][assign[2].find("until ") + len("until "):]
            index = time_str.find(",")
            substr = time_str[index: index + 5]
            time_str = time_str.replace(substr, '')
            time_str_formatted = time_str + " " + str(date.today().year)

            time_obj = datetime.strptime(time_str_formatted, '%H:%M, %b %d %Y')
            final_time_str = time_obj.isoformat()

            index_val = this_class[0].find(",")
            class_string = this_class[0][:index_val]

            event_dictionary = {
                    'name': assign[0] + ": " + assign[1],
                    'type': 'Needs to be manually sorted',
                    'course': class_string,
                    "start date": final_time_str,
                    "end date": final_time_str,
                    "start date and time": final_time_str,
                    "end date and time": final_time_str,
                    "end timestamp": final_time_str,
                    "source_name": "prairielearn"
            }

            assignments_list.append(event_dictionary)

        return assignments_list
    
    @staticmethod
    def matches_source(link):
        return 'prairielearn' in link