#! /usr/bin/env python3
import requests
from libmysql8 import mysqlHeader, mysqlBase
from lxml import etree
import hashlib
import re


class article(object):
    def __init__(self):
        self.title = ""
        self.author = ""
        self.content = ""
        self.date = None
        self.source = ""

    def _get_date(self, html):
        date_string = html.xpath("//div[@class='post_time_source']/text()")
        for s in date_string:
            result = re.search(r'\d{4}\-\d{2}\-\d{2}', s)
            if result:
                return result[0]
        return None

    def _get_title(self, html):
        title = html.xpath("//div/h1/text()")
        if title:
            title = title[0]
        return title

    def _get_source(self, html):
        source = html.xpath("//div[@class='ep-source cDGray']/span[@class='left']/text()")
        if source:
            result = re.split(r'：', source[0])
            return result[1]
        else:
            return None

    def _get_author(self, html):
        author = html.xpath("//span[@class='ep-editor']/text()")
        if author:
            result = re.split(r'：', author[0])
            return result[1]
        else:
            return None

    def _text_clean(self, text):
        content = ''
        for line in text:
            result = line.xpath(
                "./text()"
                "|.//*[name(.)='font' or name(.)='b' or name(.)='a']/text()")
            for subline in result:
                content += subline
        # remove space
        content.replace(' ', '')
        content.replace('\content', '')
        content.replace('\n', '')
        # remove \content \n etc.
        return content


start_url = "https://money.163.com"
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
