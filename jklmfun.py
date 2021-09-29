from selenium import webdriver
driver = webdriver.Chrome()
code = input()
driver.get('jklm.fun/' + code)