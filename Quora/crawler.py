from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import time
import os

def CrawlSearch():
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

def ParserSearch():
    f = open("search_result.html", "r")
    html = f.read()
    soup = BeautifulSoup(html, 'html5lib')
    url_divs = soup.find_all("a", class_="question_link")

    f_url = open("url_list.txt","w")
    for element in url_divs:
        f_url.write(element['href']+'\n')
    f_url.close()

    question_divs = soup.find_all("span", class_="ui_qtext_rendered_qtext")
    f_question = open("question_list.txt", "w")
    for element in question_divs:
        line = element.get_text()
        f_question.write(line+'\n')
    f_question.close()

if __name__ == "__main__":
    ParserSearch()