import feedparser
import requests
from bs4 import BeautifulSoup


rss_url = 'https://112ua.tv/rsslist'
rss_text = requests.get(rss_url).text
soup = BeautifulSoup(rss_text, 'html.parser')

for a in soup.find('div', class_='statpage-content').findChildren('a')[:1]:
    rss_link = a['href']
    parser = feedparser.parse(rss_link)
    print(parser.feed)
