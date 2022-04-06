from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


driver = webdriver.Chrome(ChromeDriverManager().install())

with open("secret.txt", "r") as f:
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
