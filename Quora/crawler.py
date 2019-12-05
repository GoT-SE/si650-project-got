#%%
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import time
import os

#%%
# This cell crawl questions under the search

questions_url = []
os.environ["webdriver.chrome.driver"] = "chromedriver"
browser = webdriver.Chrome()
browser.get("https://www.quora.com/search?q=game+of+throne+review")

# load html of the search page
src_updated = browser.page_source
src = ""
while src != src_updated:
    time.sleep(3)
    src = src_updated
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    src_updated = browser.page_source
html_source = browser.page_source
f = open("search_result.html","w")
f.write(html_source)
f.close()
browser.quit()

#%%
# parse the html for questions and urls
soup = BeautifulSoup(html_source)
url_divs = soup.find_all("question_link")
question_divs = soup.find_all("ui_qtext_rendered_qtext")
print(url_divs)


    # browser.get("https://www.quora.com")
    # input = browser.find_element_by_id("__w2_wbOSQ6e012_input")
    # input.sendkeys(kw)
    # input.sendkeys(Keys.ENTER)
    # wait = WebDriverWait(browser, 10)
    # wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    # print(browser.current_url)

