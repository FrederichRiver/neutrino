#! /usr/bin/env python3
import requests
from libmysql8 import mysqlHeader, mysqlBase
from lxml import etree
import hashlib
import re
from model import article
from libexception import UrlFormatError


__version__ = '1.0.1'


class spider(object, mysqlBase):
    def __init__(self):
        self.start_url = None

    def fetch_start_url(self, url):
        if re.match(r'(https?)://.', url):
            self.start_url = url
        else:
            raise UrlFormatError

    def query_url(self, url):
        # query whether url exists.
        return True

start_url = "https://money.163.com"
s = spider()
s.fetch_start_url(start_url)
md5 = hashlib.md5()
header = mysqlHeader('root', '6414939', 'spider')
mysql = mysqlBase(header)
content = requests.get(start_url)
html = etree.HTML(content.text)
href = html.xpath("//a/@href")
article_set = []
for url in href:
    if re.match(r'^http.://money.163.com/\d{2}/\d{4}/\d{2}', url):
        art = article()       
        text = requests.get(url)
        h = etree.HTML(text.text)
        content = h.xpath("//div[@class='post_text']/p/text()")
        # content = h.xpath("//body/*/text()")
        art.title = art._get_title(h)
        art.author = art._get_author(h)
        art.date = art._get_date(h)
        art.source = art._get_source(h)
        content = h.xpath("//div[@class='post_text']/p")
        art.content = art._text_clean(content)
        # print("content", art.content)
        if art.title:
            article_set.append(art)
    else:
        pass
        # print(url)
    for art in article_set:
        print(art.title)
"""
md5.update(start_url.encode('utf8'))
umd5 = md5.hexdigest()
query = f"SELECT url from url where url='{umd5}'"
result = mysql.query(query)
# print(result)
if not result:
    # print(html.xpath("//div/text()"))
    sql = f"INSERT into url (url) values ('{umd5}')"
    # mysql.insert(sql)
"""
