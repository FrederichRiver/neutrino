#!/usr/bin/python3
from venus.stock_base import StockEventBase


class spiderBase(object):
    """
    http_user_agent(): get a Mozilla User_Agent.
    http_user_agent.random_agent(): get a random User_Agent.
    http_cookie.get_cookie(cookie_name): return a cookie by name 'cookie_name'.
    """
    def __init__(self, mysql_header):
        import requests
        from jupiter.network import userAgent, cookie
        from polaris.mysql8 import mysqlBase
        self.mysql = mysqlBase(mysql_header)
        self.http_user_agent = userAgent()
        self.http_cookie = cookie()
        self.request = requests
        self.http_header = {
            "Accept": 'application/json, text/javascript, */*; q=0.01',
            "Accept-Encoding": 'gzip, deflate',
            "Accept-Language": 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            "Connection": 'keep-alive',
            "Content-Length": '155',
            "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
            # "Cookie": 'JSESSIONID=196ABC7DC9783A9A5F1183F0FC14F909; _sp_ses.2141=*; cninfo_user_browse=603019,9900023134,%E4%B8%AD%E7%A7%91%E6%9B%99%E5%85%89; UC-JSESSIONID=C5797E04FA706DCDB026811F21AFF7CA; _sp_id.2141=12284594-c734-478d-82ca-0a1ccbb7de3f.1585407313.1.1585407329.1585407313.107d6c9a-afa9-4539-a924-b01124669401',
            "Cookie": 'JSESSIONID=8B6638DD0C83CD4AB10F76F86112CF43; cninfo_user_browse=603019,9900023134,%E4%B8%AD%E7%A7%91%E6%9B%99%E5%85%89; _sp_ses.2141=*; UC-JSESSIONID=D3B1EA13B965985C23366FCB9DB4B0FC; _sp_id.2141=12284594-c734-478d-82ca-0a1ccbb7de3f.1585407313.2.1585441676.1585408733.e3950f09-4644-4027-bec6-0dbd4bace06a',
            "Host": 'www.cninfo.com.cn',
            "Origin": 'http://www.cninfo.com.cn',
            "Referer": 'http://www.cninfo.com.cn/new/disclosure/stock?stockCode=603019&orgId=9900023134',
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            "X-Requested-With": 'XMLHttpRequest',
            }

    def test(self):
        print(self.http_user_agent())
        print(self.http_cookie.get_cookie('cninfo'))
        resp = self.request.get('http://www.163.com')
        print(resp)


class cninfoSpider(spiderBase):
    def get_stock_list(self):
        import json
        import pandas
        import re
        url = 'http://www.cninfo.com.cn/new/data/szse_stock.json'
        result = self.request.get(url, self.http_header)
        jr = json.loads(result.text)
        df = pandas.DataFrame(jr['stockList'])
        df.drop(['category'], axis=1, inplace=True)
        for index, row in df.iterrows():
            if re.match(r'^0|^3|^2', row['code']):
                row['code'] = 'SZ' + row['code']
            elif re.match(r'^6|^9', row['code']):
                row['code'] = 'SH' + row['code']
        return df

    def get_hk_stock_list(self):
        import json
        import pandas
        import re
        url = 'http://www.cninfo.com.cn/new/data/hke_stock.json'
        result = self.request.get(url, self.http_header)
        jr = json.loads(result.text)
        df = pandas.DataFrame(jr['stockList'])
        df.drop(['category'], axis=1, inplace=True)
        for index, row in df.iterrows():
            row['code'] = 'HK' + row['code']
        return df

    def get_fund_stock_list(self):
        import json
        import pandas
        import re
        url = 'http://www.cninfo.com.cn/new/data/fund_stock.json'
        result = self.request.get(url, self.http_header)
        jr = json.loads(result.text)
        df = pandas.DataFrame(jr['stockList'])
        df.drop(['category'], axis=1, inplace=True)
        for index, row in df.iterrows():
            row['code'] = 'F' + row['code']
        return df

    def get_bond_stock_list(self):
        import json
        import pandas
        import re
        url = 'http://www.cninfo.com.cn/new/data/bond_stock.json'
        result = self.request.get(url, self.http_header)
        jr = json.loads(result.text)
        df = pandas.DataFrame(jr['stockList'])
        df.drop(['category'], axis=1, inplace=True)
        for index, row in df.iterrows():
            row['code'] = 'R' + row['code']
        return df

    def _insert_stock_manager(self, df):
        from jupiter.utils import ERROR
        for index, row in df.iterrows():
            try:
                insert_sql = (
                    "INSERT IGNORE into stock_manager ("
                    "stock_code, orgId, short_code,stock_name) "
                    f"VALUES ("
                    f"'{row['code']}','{row['orgId']}',"
                    f"'{row['pinyin']}','{row['zwjc']}' )"
                    )
                self.mysql.engine.execute(insert_sql)
            except Exception as e:
                ERROR(e)

    def _update_stock_manager(self, df):
        from jupiter.utils import ERROR
        for index, row in df.iterrows():
            try:
                update_sql = (
                    "UPDATE stock_manager set "
                    f"orgId='{row['orgId']}',"
                    f"short_code='{row['pinyin']}',"
                    f"stock_name='{row['zwjc']}' "
                    f"WHERE stock_code='{row['code']}'"
                    )
                self.mysql.engine.execute(update_sql)
            except Exception as e:
                ERROR(e)


class announceSpiderBase(spiderBase):
    def _set_param(self):
        self.url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
        self.http_header = {
            "Accept": 'application/json, text/javascript, */*; q=0.01',
            "Accept-Encoding": 'gzip, deflate',
            "Accept-Language": 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            "Connection": 'keep-alive',
            "Content-Length": '155',
            "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
            # "Cookie": 'JSESSIONID=196ABC7DC9783A9A5F1183F0FC14F909; _sp_ses.2141=*; cninfo_user_browse=603019,9900023134,%E4%B8%AD%E7%A7%91%E6%9B%99%E5%85%89; UC-JSESSIONID=C5797E04FA706DCDB026811F21AFF7CA; _sp_id.2141=12284594-c734-478d-82ca-0a1ccbb7de3f.1585407313.1.1585407329.1585407313.107d6c9a-afa9-4539-a924-b01124669401',
            "Cookie": 'JSESSIONID=8B6638DD0C83CD4AB10F76F86112CF43; cninfo_user_browse=603019,9900023134,%E4%B8%AD%E7%A7%91%E6%9B%99%E5%85%89; _sp_ses.2141=*; UC-JSESSIONID=D3B1EA13B965985C23366FCB9DB4B0FC; _sp_id.2141=12284594-c734-478d-82ca-0a1ccbb7de3f.1585407313.2.1585441676.1585408733.e3950f09-4644-4027-bec6-0dbd4bace06a',
            "Host": 'www.cninfo.com.cn',
            "Origin": 'http://www.cninfo.com.cn',
            "Referer": 'http://www.cninfo.com.cn/new/disclosure/stock?stockCode=603019&orgId=9900023134',
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            "X-Requested-With": 'XMLHttpRequest',
            }
        self.form_data = 'stock=603019%2C9900023134&tabName=fulltext&pageSize=30&pageNum=1&column=sse&category=&plate=sh&seDate=&searchkey=&secid=&sortName=&sortType=&isHLtitle=true'

    def set_formdata(self, stock_code, flag, i):
        flag1 = '9900023134'
        form_data = {
            "stock": f'{stock_code[2:]}%2C{flag}',
            "tabName": 'fulltext',
            "pageSize": '30',
            "pageNum": f"{i}",
            "column": 'sse',
            "category": '',
            "plate": 'sh',
            "seDate": '',
            "searchkey": '',
            "secid": '',
            "sortName": '',
            "sortType": '',
            "isHLtitle": 'true'
        }
        result = ''
        temp = []
        for k, v in form_data.items():
            line = k + '=' + v
            temp.append(line)
        result = '&'.join(temp)
        print(result)
        return result

    def set_http_header(self, stock_code, flag):
        self.http_header["Referer"] = f"http://www.cninfo.com.cn/new/disclosure/stock?stockCode={stock_code[2:]}&orgId={flag}"

    def set_cookie(self):
        pass

    def get_cookie(self):
        pass

    def run(self):
        self.form_data = self.set_formdata('SH601818', '9900006246', 1)
        self.set_http_header('SH601818', '9900006246')
        resp = self.request.post(self.url, data=self.form_data, headers=self.http_header)
        print(resp.text)


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    # event = announceSpiderBase()
    # event._set_param()
    # event.run()
    # event = spiderBase()
    # event.test()
    event = cninfoSpider(GLOBAL_HEADER)
    # df = event.get_stock_list()
    # df = event.get_hk_stock_list()
    df = event.get_fund_stock_list()
    for index, row in df.iterrows():
        print(row['code'], row['zwjc'])
    # event._insert_stock_manager(df)
    # event._update_stock_manager(df)
