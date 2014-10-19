#!/usr/bin/env python
# encoding: utf-8
# dmhy-magdl.py -- command-downloader for share.dmhy.org

import sys
import urllib
import urllib2
from datetime import datetime, timedelta
import webbrowser
import xml.etree.ElementTree as ElementTree

try:
    from babel.dates import format_timedelta
except:
    format_timedelta = None

try:
    from blessings import Terminal
except ImportError, e:
    class Terminal(object):
        def __getattr__(self, name):
            def _missing(*args, **kwargs):
                return ''.join(args)
            return _missing


# globals
t = Terminal()


def query(keyword):
    url = 'http://share.dmhy.org/topics/rss'
    params = urllib.urlencode(dict(keyword=keyword))
    request = '%s?%s' % (url, params)
    response = urllib2.urlopen(request)
    xml = response.read()

    # parsing items
    root = ElementTree.fromstring(xml)
    def _build_item(node):
        date = datetime.strptime(node.find('pubDate').text, '%a, %d %b %Y %H:%M:%S +0800') # Thu, 16 Oct 2014 20:52:51 +0800
        if format_timedelta:
            delta = datetime.now() - date
            date = format_timedelta(delta, locale='en_US')
        else:
            date = date.strftime('%m/%d %H:%M')
        return dict(
            title=node.find('title').text,
            date=date, 
            magnet=node.find("enclosure[@type='application/x-bittorrent']").get('url'))
    items = map(_build_item, root.findall('channel/item'))
    items = filter(lambda x: x['title'], items)
    return items[:24]


def ask(choices):
    for idx, item in enumerate(choices):
        num = t.red(str(idx+1).rjust(2))
        title = t.yellow(item['title'])
        date = t.green(item['date'].rjust(12))
        print '%s. %s %s' % (num, date, title)
    answers = raw_input('What items do you like? (seperated by commas) [1] ')
    if answers: return map(lambda x: int(x)-1, answers.split(r','))
    else: return [0]


def download(items):
    for item in items:
        print 'Downloading... %s' % (item['title'])
        webbrowser.open(item['magnet'])


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print 'Usage: %s <keyword>' % sys.argv[0]
        print "Example: %s 'Fate stay night' " % sys.argv[1]
        sys.exit(1)
    keyword = sys.argv[1]
    choices = query(keyword)
    chosen_ids = ask(choices)
    chosens = map(lambda idx: choices[idx], chosen_ids)
    download(chosens)
