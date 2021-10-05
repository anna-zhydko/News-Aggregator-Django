import feedparser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from fuzzywuzzy import fuzz


def get_trends():
    c = time.time()

    google_trends_url = 'https://trends.google.com/trends/trendingsearches/daily?geo=UA'
    # path = 'C:\Program Files (x86)\chromedriver'
    # driver = webdriver.Chrome()
    driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME)
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
    trends_112 = []  # the list stores all 112 news that has been matched with google trends

    # Getting records from all 112 rss lists
    for a in soup.find('div', class_='statpage-content').findChildren('a'):
        rss_link = a['href']
        parser = feedparser.parse(rss_link)  # feedparser for rss
        for entry in parser.entries:
            possible_trends = []  # the list stores google trends that could belong to the rss record
            title, link, fulltext, published = entry.title, entry.link, entry.fulltext[:100], entry.published

            # Comparing rss-record with google trend
            for trend in google_trends:
                match = fuzz.token_sort_ratio(trend['title'] + trend['subtitle'], title + fulltext)
                if match > 50:  # match should be more than 50%
                    possible_trends.append(trend['title'])

            # if 112_news has been matched at least one google trend
            if possible_trends:
                trends_112.append({'title': title, 'link': link, 'published': published,
                                   'google_trends': possible_trends})
    print(trends_112)
    print(time.time() - c)
    return trends_112


if __name__ == "__main__":
    get_trends()
