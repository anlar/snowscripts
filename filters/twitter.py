#!/usr/bin/env python3

import re
import sys
from datetime import datetime, timezone

from bs4 import BeautifulSoup

page = sys.stdin.read()
soup = BeautifulSoup(page, 'html.parser')

title = soup.html.head.title.text
link = soup.html.head.find('link', {'rel': 'canonical', 'href': True})['href']

entries = []

timeline = soup.find('div', {'id': 'timeline'})

for item in timeline.findAll('div', {'class': re.compile('.*js-stream-tweet.*')}):
    timestamp = item.find('span', {'class': re.compile('.*js-short-timestamp.*')})['data-time']
    content = item.find('p', {'class': re.compile('TweetTextSize.*')})

    for a in content.findAll('a'):
        for tag in a.findAll(recursive=False):
            tag.replaceWith(tag.text.strip())

    entry = {
        'name': item['data-name'] + ' (@' + item['data-screen-name'] + ')',
        'link': 'https://twitter.com' + item['data-permalink-path'],
        'text': content.text.strip(),
        'html': str(content),
        'updated': datetime.fromtimestamp(float(timestamp), timezone.utc).isoformat(),
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

    '''.format(title, link, entries[0]['updated'], entries[0]['name'], link, link)

    for entry in entries:
        rss += '''
        <entry>
            <title>{}</title>
            <link href="{}"/>
            <id>{}</id>
            <updated>{}</updated>
            <author>
                <name>{}</name>
                <uri>{}</uri>
            </author>
            <content type="xhtml">{}</content>
        </entry>
        '''.format(entry['text'], entry['link'], entry['link'], entry['updated'], entry['name'], link, entry['html'])

    print(rss + '</feed>')
