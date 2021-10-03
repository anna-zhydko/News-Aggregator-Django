import feedparser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# rss_url = 'https://112ua.tv/rsslist'
# rss_text = requests.get(rss_url).text
# soup = BeautifulSoup(rss_text, 'html.parser')
#
# for a in soup.find('div', class_='statpage-content').findChildren('a')[:1]:
#     rss_link = a['href']
#     parser = feedparser.parse(rss_link)
#     print(parser.feed)
c = time.time()
google_trends_url = 'https://trends.google.com/trends/trendingsearches/daily?geo=UA'
path = 'C:\Program Files (x86)\chromedriver'
driver = webdriver.Chrome(path)

driver.get(google_trends_url)

try:
    # Wait until all elements are loaded
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "generic-container-wrapper"))
    )
    date_count = 0

    # Loading all 7days-notes
    while date_count < 7:
        date_count = len(driver.find_elements_by_class_name('content-header-title'))
        # Wait until more button is loaded
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "feed-load-more-button"))
        )
        driver.find_element_by_class_name('feed-load-more-button').click()

    # Collecting information from 7days-notes
    for item in driver.find_elements_by_class_name('feed-item-header'):
        for x in item.find_elements_by_tag_name('a'):
            print(x.text)
finally:
    driver.quit()
print(time.time() - c)
