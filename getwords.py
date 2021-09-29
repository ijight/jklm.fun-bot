from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException        

word = input("Words containing:")
driver = webdriver.Chrome()

driver.get("https://www.thefreedictionary.com/words-containing-" + word)
ans = ''

def check_exists_by_id(i):
    try:
        driver.find_element_by_id(i)
    except NoSuchElementException:
        return False
    return True

for t in range(2, 20):
    id = "w" + str(t)
    if (check_exists_by_id(id)):
        elems = driver.find_element_by_id(id)
        ans += elems.text + "\n"

f = open("stored.txt", "w")
f.write(str(ans))
f.close()
