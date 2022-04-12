from calendar_source import CalendarSourceTemplate
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from scrapingant_client import ScrapingAntClient

class Prairie(CalendarSourceTemplate):
    def extract_event_info(self, event, event_dictionary):
        event_dictionary['source_name'] = "prairielearn"

        event_dictionary['name'] = "TBD"

        event_dictionary['type'] = 'Needs to be manually sorted'

        event_dictionary['course'] = "TBD"
    
    def filter_event(self, event):
        return True
    
    def request(self, f, driver):
        # Login to PL
        email = f.readline()    
        password = f.readline()    
        driver.get("https://www.prairielearn.org/")
        driver.find_element(By.LINK_TEXT, "Log in").click()
        time.sleep(5) 
        driver.find_element(By.LINK_TEXT, "Sign in with Illinois").click()
        time.sleep(5) 
        driver.find_element(By.ID, "userNameInput").send_keys(email + Keys.ENTER)
        time.sleep(5) 
        driver.find_element(By.ID, "passwordInput").send_keys(password + Keys.ENTER)
        time.sleep(5) 
    
        driver.get(self.link)
        
        # Webscrape PL
        # client = ScrapingAntClient(token='2b6ffb675d654a998e1d64e08953bdac')
        # page_source = client.general_request(self.link).content
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        assignments = []
        # get data on page
        for assignment in soup.find_all(['tr']):
            assign = []
            for attr in assignment.find_all(['td']):
                assign.append(attr.get_text().strip())
            if len(assign) > 0:
                assignments.append(assign[:len(assign)-1])
        
        test_file = open("data/" + self.link[48:] + ".txt", "w")

        for assign in assignments:
            test_file.write("\n".join(assign))
            test_file.write("\n===================\n")

        return True