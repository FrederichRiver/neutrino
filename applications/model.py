#! /usr/bin/env python3
import requests
from libmysql8 import mysqlHeader, mysqlBase
from lxml import etree
import hashlib
import re


__version__ = '1.0.1'


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
