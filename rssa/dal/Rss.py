import feedparser
from bs4 import BeautifulSoup as bs
from itertools import repeat
from datetime import datetime
import hashlib
import json
import dateutil.parser as dateparser
import pytz

def parse_publish_time(s):
    return dateparser.parse(s).astimezone(pytz.utc).strftime('%Y%m%d%H%M')

def encode(s):
    return ''.join([c if len(c.encode('utf-8')) < 4 else '' for c in s])
def parse_entry(entry, thumbnail_path = None):
    summary = bs(entry['summary'], features="lxml") if 'summary' in entry else None
    result = dict(title = entry['title'] if 'title' in entry else None,
                  link = entry['link'] if 'link' in entry else None,
                  publish_ts = parse_publish_time(entry['published']) if 'published' in entry else None,
                  summary = encode(summary.get_text()) if summary is not None else None,
                  thumbnail_link = None)
    try:
        if thumbnail_path is not None:
            if 'summary' in thumbnail_path:
                if summary.find('img'):
                    result['thumbnail_link'] = summary.img['src']
            elif 'storyimage' in thumbnail_path:
                result['thumbnail_link'] = entry['storyimage'] if 'storyimage' in entry else None
            elif 'media' in thumbnail_path:
                path = thumbnail_path.split('>')
                result['thumbnail_link'] = entry[path[0]][0][path[1]]
    except:
        pass
    result['id'] = hashlib.md5(json.dumps(result).encode("utf-8")).hexdigest()
    return result

def read(rss, thumbnail):
    feed = feedparser.parse(rss)
    result = list(map(parse_entry, feed.entries, repeat(thumbnail)))
    return result