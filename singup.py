from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import re
import random

driver = webdriver.Chrome()
driver.get("https://jklm.fun/") 
driver.find_element_by_css_selector('body').send_keys(Keys.TAB + Keys.TAB + Keys.ENTER)
time.sleep(1)
