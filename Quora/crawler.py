import bs4
import requests
from selenium import webdriver

def CrawlQuestions(kw):
    browser = webdriver.Chrome()
    browser.get("https://www.quora.com")
    input = browser.find_element_by_id("__w2_wbOSQ6e012_input")
    

if __name__ == "__main__":
    kw = 
    CrawlQuestions(kw)
