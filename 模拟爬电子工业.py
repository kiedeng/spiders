import requests
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Chrome()
url = "https://yd.51zhy.cn/ebook/reader/index.html#/pdfReader?id=622504"
browser.maximize_window()
element = browser.find_element_by_xpath('//*[@id="the-canvas0"]')
ac = ActionChains(browser)
ac.move_to_element(element)
ac.perform()
browser.get(url)

while 1:
    time.sleep(3)
    browser.execute_script('window.scrollBy(0,1000)')
