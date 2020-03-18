#! /usr/bin/env python3
import hashlib
import re
import requests
from lxml import etree
from polaris.mysql8 import mysqlHeader, mysqlBase
from sqlalchemy import Column, String, Integer, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base


__version__ = '1.0.2'


article_base = declarative_base()


class spider(object):
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


class formArticle(article_base):
    __tablename__ = 'article'
    idx = Column(Integer)
    title = Column(String(50), primary_key=True)
    url = Column(String(50))
    author = Column(String(20))
    release_date = Column(Date)
    source = Column(String(20))
    content = Column(Text)


class article(object):
    def __init__(self):
        self.title = ""
        self.author = ""
        self.content = ""
        self.date = None
        self.source = ""
        self.url = ""

    def _get_date(self, html):
        import lxml
        if not isinstance(html, lxml.etree._Element):
            raise TypeError('html type error')
        date_string = html.xpath("//div[@class='post_time_source']/text()")
        for s in date_string:
            result = re.search(r'\d{4}\-\d{2}\-\d{2}', s)
            if result:
                return result[0]
        return None

    def _get_title(self, html):
        import lxml
        if not isinstance(html, lxml.etree._Element):
            raise TypeError('html type error')
        title = html.xpath("//div/h1/text()")
        if title:
            title = title[0]
        return title

    def _get_source(self, html):
        import lxml
        if not isinstance(html, lxml.etree._Element):
            raise TypeError('html type error')
        source = html.xpath("//div[@class='ep-source cDGray']/span[@class='left']/text()")
        if source:
            result = re.split(r'：', source[0])
            return result[1]
        else:
            return None

    def _get_author(self, html):
        import lxml
        if not isinstance(html, lxml.etree._Element):
            raise TypeError('html type error')
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


if __name__ == "__main__":
    pass
