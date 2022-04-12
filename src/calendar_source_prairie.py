from calendar_source import CalendarSourceTemplate
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

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
        driver.get(self.link)
        driver.find_element(By.LINK_TEXT, "Log in").click()
        time.sleep(5) 
        driver.find_element(By.LINK_TEXT, "Sign in with Illinois").click()
        time.sleep(5) 
        driver.find_element(By.ID, "userNameInput").send_keys(email + Keys.ENTER)
        time.sleep(5) 
        driver.find_element(By.ID, "passwordInput").send_keys(password + Keys.ENTER)
        time.sleep(5) 

        # Webscrape PL
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        return True