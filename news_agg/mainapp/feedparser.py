import feedparser
import requests
from bs4 import BeautifulSoup


rss_url = 'https://112ua.tv/rsslist'
rss_text = requests.get(rss_url).text
soup = BeautifulSoup(rss_text, 'html.parser')
list_ = soup.find('div', class_='statpage-content')
print(list_)