from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

def getClassLinks(f, driver):
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

    # Webscrape PL
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    links = []
    # get all links on page
    for link in soup.find_all('a'):
        # display the actual urls
        l = link.get('href')
        if l.find("course_instance") != -1:
            links.append("https://www.prairielearn.org" + l)

    return links