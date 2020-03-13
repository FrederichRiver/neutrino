#!/usr/bin/python3

from taurus.news_downloader import newsSpider
from polaris.mysql8 import mysqlHeader
from dev_global.env import SOFT_PATH


def event_download_netease_news():
    header = mysqlHeader('stock', 'stock2020', 'natural_language')
    event = newsSpider(header, SOFT_PATH)
    event.generate_url_list()
    for url in event.url_list:
        event.extract_href(url)
    event.save_process()
    # hfile = SOFT_PATH + 'config/HREF_LIST'
    # event.load_href_file(hfile)
    for url in event.href:
        art = event.extract_article(url)
        event.record_article(art)
