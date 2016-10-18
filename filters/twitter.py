#!/usr/bin/env python3

import re, sys
import urllib.request
from datetime import datetime, timezone

from bs4 import BeautifulSoup


url = sys.argv[1]

entries = []

req = urllib.request.Request(url)

with urllib.request.urlopen(req, timeout=30) as response:
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')

    title = soup.html.head.title.text

    timeline = soup.find('div', {'id': 'timeline'})

    for item in timeline.findAll('div', {'class': re.compile('.*js-stream-tweet.*')}):
        timestamp = item.find('span', {'class': re.compile('.*js-short-timestamp.*')})['data-time']

        entry = {
            'name': item['data-name'] + ' (@' + item['data-screen-name'] + ')',
            'link': 'https://twitter.com' + item['data-permalink-path'],
            'text': item.find('p', {'class': re.compile('TweetTextSize.*')}).text.strip(),
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

    '''.format(title, url, entries[0]['updated'], entries[0]['name'], url, url)

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
            <content>{}</content>
        </entry>
        '''.format(entry['text'], entry['link'], entry['link'], entry['updated'], entry['name'], url, entry['text'])

    print(rss + '</feed>')
