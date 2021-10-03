import feedparser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from fuzzywuzzy import fuzz

c = time.time()

google_trends_url = 'https://trends.google.com/trends/trendingsearches/daily?geo=UA'
path = 'C:\Program Files (x86)\chromedriver'
driver = webdriver.Chrome(path)
google_trends = []

driver.get(google_trends_url)

try:
    # Wait until all elements are loaded
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "generic-container-wrapper"))
    )
    date_count = 0

    # Loading all 7days-records
    while date_count < 7:
        date_count = len(driver.find_elements_by_class_name('content-header-title'))
        # Wait until more button is loaded
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "feed-load-more-button"))
        )
        driver.find_element_by_class_name('feed-load-more-button').click()

    # Collecting information from 7days-records
    for item in driver.find_elements_by_class_name('feed-item-header'):
        item_parts = item.find_elements_by_tag_name('a')
        title, subtitile = item_parts[0].text, item_parts[1].text
        google_trends.append({'title': title, 'subtitle': subtitile})
finally:
    driver.quit()

rss_url = 'https://112ua.tv/rsslist'
rss_text = requests.get(rss_url).text
soup = BeautifulSoup(rss_text, 'html.parser')
possible_trends = []  # the list stores google trends that could belong to the rss record

# Getting records from all 112 rss lists
for a in soup.find('div', class_='statpage-content').findChildren('a'):
    rss_link = a['href']
    parser = feedparser.parse(rss_link)  # feedparser for rss
    for entry in parser.entries:
        title, link, fulltext, published = entry.title, entry.link, entry.fulltext[:100], entry.published

        # Comparing rss-record with google trend
        for trend in google_trends:
            match = fuzz.token_sort_ratio(trend['title'] + trend['subtitle'], title + fulltext)
            if match > 50:  # match should be more than 50%
                google_trends.append(trend['title'])
                # print('112', title.lower() + fulltext)
                # print('trend', trend['title'].lower() + trend['subtitle'].lower())
                # print('match', match)


print(time.time() - c)
