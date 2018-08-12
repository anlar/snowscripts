#!/usr/bin/env python3

import re
from datetime import datetime
from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup

home_url = 'https://www.tinkoff.ru/'
news_url = 'https://www.tinkoff.ru/about/news/'
archive_url = 'https://www.tinkoff.ru/about/news-archive/'

page = urlopen(archive_url).read()
soup = BeautifulSoup(page, 'html.parser')

title = soup.html.head.find('meta', {'property': 'og:site_name'})['content']
link = soup.html.head.find('link', {'rel': 'canonical', 'href': True})['href']

entries = []

timeline = soup.find('ul', {'data-qa-file': 'NewsArchivePage'})

for item in timeline.findAll('span', {'class': 'ui-link'}):
    href = item.find('a', {'data-qa-file': 'Link'}, href=True)['href']
    updated = re.search('/about/news/(\d*)-(.*)', href).group(1)

    entry = {
        'title': item.find('span', {'data-qa-file': 'NewsArchiveItem'}).text,
        'link': urljoin(news_url, href),
        'updated': datetime.strptime(updated, "%d%m%Y")
    }

    entries.append(entry)

if entries:
    rss = '''<?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">

        <title>{}</title>
        <link href="{}"/>
        <updated>{}</updated>
        <author>
            <name>{}</name>
            <uri>{}</uri>
        </author>
        <id>{}</id>

    '''.format(title, link, entries[0]['updated'], title, home_url, link)

    for entry in entries:
        rss += '''
        <entry>
            <title>{}</title>
            <link rel="alternate" href="{}"/>
            <id>{}</id>
            <updated>{}</updated> 
            <author>
                <name>{}</name>
                <uri>{}</uri>
            </author>
            <content> </content>
        </entry>
        '''.format(entry['title'], entry['link'], entry['link'], entry['updated'], title, home_url)

    print(rss + '</feed>')
