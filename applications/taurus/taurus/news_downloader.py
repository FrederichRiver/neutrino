#! /usr/bin/env python3
import hashlib
import json
import re
import requests
from lxml import etree
from jupiter.utils import ERROR
from taurus.model import article
from polaris.mysql8 import mysqlHeader, mysqlBase
from sqlalchemy import Column, String, Integer, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base


__version__ = 1

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


class newsSpider(object):
    def __init__(self, header, path):
        self.mysql = mysqlBase(header)
        self.url_list = []
        self.href = []
        self.article_set = []
        self.path = path + 'config/'

    def save_process(self):
        url_file = self.path + 'URL_LIST'
        with open(url_file, 'w') as f:
            for url in self.url_list:
                f.write(str(url) + '\n')
        href_file = self.path + 'HREF_LIST'
        with open(href_file, 'w') as f:
            for url in self.href:
                f.write(str(url) + '\n')

    def generate_url_list(self):
        self._chn_list()
        self._hk_list()
        self._us_list()
        self._ipo_list()
        self._fund_list()
        self._future_list()
        self._kcb_list()
        self._forexchange_list()
        self._chairman_list()
        self._bc_list()

    def _chn_list(self):
        chn_start_url = "https://money.163.com/special/002557S6/newsdata_gp_index.js?callback=data_callback"
        self.url_list.append(chn_start_url)
        chn_url_list = [f"https://money.163.com/special/002557S6/newsdata_gp_index_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += chn_url_list

    def _hk_list(self):
        hk_start_url = "https://money.163.com/special/002557S6/newsdata_gp_hkstock.js?callback=data_callback"
        self.url_list.append(hk_start_url)
        hk_url_list = [f"https://money.163.com/special/002557S6/newsdata_gp_hkstock_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += hk_url_list

    def _us_list(self):
        us_start_url = "https://money.163.com/special/002557S6/newsdata_gp_usstock.js?callback=data_callback"
        self.url_list.append(us_start_url)
        us_url_list = [f"https://money.163.com/special/002557S6/newsdata_gp_usstock_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += us_url_list

    def _ipo_list(self):
        ipo_start_url = "https://money.163.com/special/002557S6/newsdata_gp_ipo.js?callback=data_callback"
        self.url_list.append(ipo_start_url)
        ipo_url_list = [f"https://money.163.com/special/002557S6/newsdata_gp_ipo_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += ipo_url_list

    def _future_list(self):
        qhzx_start_url = "https://money.163.com/special/002557S6/newsdata_gp_qhzx.js?callback=data_callback"
        self.url_list.append(qhzx_start_url)
        qhzx_url_list = [f"https://money.163.com/special/002557S6/newsdata_gp_qhzx_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += qhzx_url_list

    def _forexchange_list(self):
        forex_start_url = "https://money.163.com/special/002557S6/newsdata_gp_forex.js?callback=data_callback"
        self.url_list.append(forex_start_url)
        forex_url_list = [f"https://money.163.com/special/002557S6/newsdata_gp_forex_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += forex_url_list

    def _bc_list(self):
        bitcoin_start_url = "https://money.163.com/special/002557S6/newsdata_gp_bitcoin.js?callback=data_callback"
        self.url_list.append(bitcoin_start_url)
        bitcoin_url_list = [f"https://money.163.com/special/002557S6/newsdata_gp_bitcoin_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += bitcoin_url_list

    def _kcb_list(self):
        kcb_start_url = "http://money.163.com/special/00259D2D/fund_newsflow_hot.js?callback=data_callback"
        self.url_list.append(kcb_start_url)
        kcb_url_list = [f"http://money.163.com/special/00259D2D/fund_newsflow_hot_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += kcb_url_list

    def _fund_list(self):
        fund_start_url = "http://money.163.com/special/00259CPE/data_kechuangban_kechuangban.js?callback=data_callback"
        self.url_list.append(fund_start_url)
        fund_url_list = [f"http://money.163.com/special/00259CPE/data_kechuangban_kechuangban_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += fund_url_list

    def _chairman_list(self):
        chairman_start_url = "http://money.163.com/special/00259CTD/data-yihuiman.js?callback=data_callback"
        self.url_list.append(chairman_start_url)
        chairman_url_list = [f"http://money.163.com/special/00259CTD/data-yihuiman_0{i}.js?callback=data_callback" for i in range(2, 10)]
        self.url_list += chairman_url_list

    def extract_href(self, url):
        resp = requests.get(url)
        result = re.findall(
            r'\"docurl\":\"(http.://money.163.com/\d{2}/\d{4}/\d{2}/\w+\.html)\"',
            resp.text)
        self.href += result

    def extract_article(self, url):
        try:
            art = article()
            text = requests.get(url)
            h = etree.HTML(text.text)
            content = h.xpath("//div[@class='post_text']/p/text()")
            art.url = url
            art.title = art._get_title(h)
            art.author = art._get_author(h)
            art.date = art._get_date(h)
            art.source = art._get_source(h)
            content = h.xpath("//div[@class='post_text']/p")
            art.content = art._text_clean(content)
        except Exception as e:
            ERROR("Extract article failed.")
            ERROR(e)
        return art

    def record_article(self, art):
        try:
            insert_data = {
                'title': f"{art.title}",
                'url': f"{art.url}",
                'release_date': f"{art.date}",
                'author': f"{art.author}",
                'source': f"{art.source}",
                'content': f"{art.content}"
                }
            self.mysql.session.execute(
                formArticle.__table__.insert().prefix_with('IGNORE'),
                insert_data)
            self.mysql.session.commit()
        except Exception as e:
            print(e)

    def load_href_file(self, href_file):
        try:
            with open(href_file, 'r') as f:
                url = f.readline()
                # print(url)
                self.href.append(url)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    from dev_global.env import SOFT_PATH
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
