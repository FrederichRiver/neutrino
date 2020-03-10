#! /usr/bin/env python3
import requests
from polaris.mysql8 import mysqlHeader, mysqlBase
from lxml import etree
import hashlib
import re
from model import article
from sqlalchemy import Column, String, Integer, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base


__version__ = '1.0.1'

Base = declarative_base()


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


class formArticle(Base):
    __tablename__ = 'article'
    idx = Column(Integer)
    title = Column(String(50), primary_key=True)
    url = Column(String(50))
    author = Column(String(20))
    release_date = Column(Date)
    source = Column(String(20))
    content = Column(Text)


start_url = "https://money.163.com"
s = spider()
s.fetch_start_url(start_url)
md5 = hashlib.md5()
header = mysqlHeader('stock', 'stock2020', 'nature_language')
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
        art.url = url
        art.title = art._get_title(h)
        art.author = art._get_author(h)
        art.date = art._get_date(h)
        art.source = art._get_source(h)
        content = h.xpath("//div[@class='post_text']/p")
        art.content = art._text_clean(content)
        # print("content", art.content)
        if art.title:
            article_set.append(art)
    for art in article_set:
        print(art.title)
        arti = formArticle(
            title=f"{art.title}", url=f"{art.url}", content=f"{art.content}")
        insert_data = {
            'title': f"{art.title}", 'url': f"{art.url}",
            'content': f"{art.content}",'release_date': f"{art.date}",
            'author': f"{art.author}", 'source': f"{art.source}"
        }
        mysql.session.execute(
            formArticle.__table__.insert().prefix_with('IGNORE'),
            insert_data)
        mysql.session.commit()
        sql = (
            f"INSERT IGNORE into article ("
            f"title, url, author, release_date, source, content ) "
            "VALUES ("
            f"md5('{art.title}'),'{art.url}','{art.author}',"
            f"'{art.date}','{art.source}',{art.content.encode('utf-8')})"
        )
        try:
            pass
            # mysql.engine.execute(sql)
        except Exception as e:
            print(sql)



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
