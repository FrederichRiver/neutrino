#!/usr/bin/python3

"""
Geschafen im Feb 13, 2019
Verfasst von Friederich Fluss
Version
v1.1.4, Feb 13, 2019, rebuild this lib.
v1.2.5, Feb 17, 2019, build class stockeventbase, not perfect.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pywt
import random
import re
import requests
import talib as ta
import time
from datetime import datetime
from enum import Enum
from env import TIME_FMT, CONF_FILE
from form import formStockList
from lxml import etree
from libmysql8 import (mysqlBase, mysqlHeader,
                       create_table_from_table)
from message import ADJUST_FACTOR_ERROR
from sqlalchemy.types import Date, DECIMAL, Integer, NVARCHAR
from utils import read_json, neteaseindex, today, info, error

__version__ = '1.7.33'


def wavelet_nr(df):
    """TODO: Docstring for wavelet_nr.

    :df: TODO
    :returns: TODO

    """
    db4 = pywt.Wavelet('db4')
    coeffs = pywt.wavedec(df, db4)
    coeffs[-1] *= 0
    coeffs[-2] *= 0
    meta = pywt.waverec(coeffs, db4)
    return meta


class SecurityFlag(Enum):
    index = 0
    stock = 1
    fund = 2
    future = 3


class StockEventBase(object):
    def __init__(self):
        self.queue = []
        self.code = {}
        self.Today = datetime.now().strftime(TIME_FMT)
        self.mysql = None
        self.stock_list = []
        self.security_list = []
        self.coder = codeFormat()

    def __str__(self):
        return "class <Stock Event Base>"

    def _init_database(self, header):
        self.mysql = mysqlBase(header)

    def update_date_time(self):
        self.Today = datetime.now().strftime(TIME_FMT)

    def fetch_all_stock_list(self):
        self.stock_list = []
        result = self.mysql.session.query(
            formStockList.stock_code, formStockList.flag).all()
        for dataline in result:
            # flag = 1 means stock
            if dataline[1] == '1':
                self.stock_list.append(dataline[0])
        return self.stock_list

    def fetch_all_security_list(self):
        # Return all kinds of securities in form stock list.
        self.security_list = []
        result = self.mysql.session.query(
            formStockList.stock_code).all()
        for dataline in result:
            if dataline[0]:
                self.security_list.append(dataline[0])
        return self.security_list

    def fetch_no_flag_stock(self):
        result = self.mysql.session.query(
            formStockList.stock_code).all()
        stock_list = []
        for stock in result:
            if stock[0]:
                stock_list.append(stock[0])
        return stock_list

    def close(self):
        self.mysql.engine.close()


class EventStockPrice(StockEventBase):
    def run(self, code, field):
        prices = self.mysql.select_values(code, field)
        df = pd.DataFrame(list(prices), columns=field.split(','))
        return df


class EventFlag(StockEventBase):
    def main_flag(self, stock_code):
        if re.match(r'^SH0|^SZ9', stock_code):
            self._flag_index(stock_code)
        elif re.match(r'^SH6', stock_code):
            self._flag_stock(stock_code)
        elif re.match(r'^SZ[0|3|8]', stock_code):
            self._flag_stock(stock_code)
        else:
            pass

    def _flag_index(self, stock_code):
        stock_name = fetch_name(stock_code)
        result = self.mysql.session.query(
            formStockList.stock_code,
            formStockList.flag
            ).filter_by(stock_code=stock_code)
        if result:
            result.update(
                {"flag": '0'}
            )
            self.mysql.session.commit()
        return 1

    def _flag_stock(self, stock_code):
        # format '1,S,<1.1,1.2,3.7>'
        # 1- Stock, S(special treat, including double stars),
        # numbers in '<>' means hangye, 1st class and 2nd class)
        # st, stop
        stock_name = fetch_name(stock_code)
        result = self.mysql.session.query(
            formStockList.stock_code,
            formStockList.flag
            ).filter_by(stock_code=stock_code)
        if result:
            result.update(
                {"flag": '1'}
            )
            self.mysql.session.commit()
        return 1

    def fetch_name(self, s):
        pass

    def _flag_fund(self, stock_code):
        pass

    def _flag_future(self, stock_code):
        pass

    def _flag_gold(self, stock_code):
        pass

    def _flag_right(self, stock_code):
        pass


def fetch_name(s):
    pass


class EventTradeDataManager(StockEventBase):
    def __init__(self):
        super(StockEventBase, self).__init__()
        self.coder = codeFormat()

    def fetch_trade_data_from_netease(
            self, code, start_date='19901219', end_date=today()):
        """
        read csv data and return a dataframe object.
        """
        # config file is a url file.
        _, url = read_json('URL_163_MONEY', CONF_FILE)
        query_code = self.coder.net_ease_code(code)
        netease_url = url.format(query_code, start_date, end_date)
        return pd.read_csv(netease_url, encoding='gb18030')

    def fetch_stock_name(self, code):
        try:
            result = self.fetch_data_from_netease(code)
            if len(result) > 0:
                stock_name = result.iloc[1, 2].replace(' ', '')
            else:
                stock_name = None
        except Exception as e:
            print(f"{time.ctime()}: Error when fetching stock name. {e}")
            stock_name = None
        return code, stock_name

    def record_stock(self, stock_code):
        result = self.check_stock(stock_code)
        if result is None:
            self.create_stock_table(stock_code)

    def check_stock(self, stock_code):
        # It is a sub function of _record_stock
        result = self.mysql.session.query(
            formStockList.stock_code
        ).filter_by(stock_code=stock_code).first()
        return result

    def create_stock_table(self, code):
        stock_code, stock_name = self.fetch_stock_name(code)
        if stock_name:
            stock_orm = formStockList(stock_code=stock_code,
                                      stock_name=stock_name,
                                      gmt_create=datetime.today())
            self.mysql.session.add(stock_orm)
            self.mysql.session.commit()
            create_table_from_table(stock_code,
                                    'template_stock',
                                    self.mysql.engine)

    def _data_cleaning(self, df):
        df.drop(['stock_code'], axis=1, inplace=True)
        df.replace('None', np.nan, inplace=True)
        df = df.dropna(axis=0, how='any')

    def init_stock_data(self, stock_code):
        """
        used when first time download stock data.
        """
        result = self.fetch_trade_data_from_netease(stock_code)
        result.columns = ['trade_date', 'stock_code',
                          'stock_name', 'close_price',
                          'highest_price', 'lowest_price',
                          'open_price', 'prev_close_price',
                          'change_rate', 'amplitude',
                          'volume', 'turnover']
        result = self._data_cleaning(result)
        columetype = {
            'trade_date': Date,
            'stock_name': NVARCHAR(length=10),
            'close_price': DECIMAL(7, 3),
            'highest_price': DECIMAL(7, 3),
            'lowest_price': DECIMAL(7, 3),
            'open_price': DECIMAL(7, 3),
            'prev_close_price': DECIMAL(7, 3),
            'change_rate': DECIMAL(7, 3),
            'amplitude': DECIMAL(7, 4),
            'volume': Integer(),
            'turnover': DECIMAL(20, 2)
        }
        # stk = formStockList(stock_code=stock_code,
        #            gmt_modified=datetime.today())
        # engine.session.add(stk)
        # engine.session.commit()
        try:
            result.to_sql(name=stock_code,
                          con=self.mysql.engine,
                          if_exists='append',
                          index=False,
                          dtype=columetype)
            query = self.mysql.session.query(
                formStockList.stock_code,
                formStockList.gmt_modified
            ).filter_by(stock_code=stock_code)
            if query:
                query.update(
                    {"gmt_modified": today()})
            self.mysql.session.commit()
        except Exception as e:
            print(f'{time.ctime()}: Error 3 - {e}')

    def download_stock_data(self, stock_code):
        # print(stock_code)
        result = self._get_file_from_net_ease(stock_code)
        result.columns = ['trade_date', 'stock_code',
                          'stock_name', 'close_price',
                          'highest_price', 'lowest_price',
                          'open_price', 'prev_close_price',
                          'change_rate', 'amplitude',
                          'volume', 'turnover']
        result = self._data_cleaning(result)
        columetype = {
            'trade_date': Date,
            'stock_name': NVARCHAR(length=10),
            'close_price': DECIMAL(7, 3),
            'highest_price': DECIMAL(7, 3),
            'lowest_price': DECIMAL(7, 3),
            'open_price': DECIMAL(7, 3),
            'prev_close_price': DECIMAL(7, 3),
            'change_rate': DECIMAL(7, 3),
            'amplitude': DECIMAL(7, 4),
            'volume': Integer(),
            'turnover': DECIMAL(20, 2)
        }
        # stk = formStockList(stock_code=stock_code,
        #            gmt_modified=datetime.today())
        # engine.session.add(stk)
        # engine.session.commit()
        from datetime import date
        try:
            sql = f"SELECT trade_date from {stock_code}"
            query = self.mysql.engine.execute(sql).fetchall()
            result['trade_date'] = pd.to_datetime(result['trade_date'], format=TIME_FMT)
            result = result.sort_values('trade_date')
            # print(result.head(5))
            t2 = query[-1][0]
            update_date = t2
            for index, row in result.iterrows():
                t1 = row['trade_date'].to_pydatetime().date()
                if t1 > t2:
                    sql2 = (
                        f"INSERT into {stock_code} "
                        "(trade_date,stock_name,close_price,"
                        "highest_price,lowest_price,open_price,prev_close_price,"
                        "change_rate,amplitude,volume,turnover)"
                        f"VALUES('{row['trade_date']}','{row['stock_name']}',"
                        f"{row['close_price']},{row['highest_price']},"
                        f"{row['lowest_price']},{row['open_price']},"
                        f"{row['prev_close_price']},{row['change_rate']},"
                        f"{row['amplitude']},{row['volume']},{row['turnover']})")    
                    self.mysql.engine.execute(sql2)
                    update_date = t1
            query = self.mysql.session.query(
                        formStockList.stock_code,
                        formStockList.gmt_modified
                    ).filter_by(stock_code=stock_code)
            if query:
                query.update(
                    {"gmt_modified": update_date})
            self.mysql.session.commit()
        except Exception as e:
            print(f'{time.ctime()}: Error 3 - {e}')


class EventCreateInterestTable(StockEventBase):
    def create_interest_table(self):
        from form import formInterest
        self.fetch_all_stock_list()
        for stock_code in self.stock_list:
            print(f"{time.ctime()}: Create interest table {stock_code}")
            create_table_from_table(
                f"{stock_code}_interest",
                formInterest.__tablename__,
                self.mysql.engine)


class EventRecordInterest(StockEventBase):
    def record_interest(self):
        self.fetch_all_stock_list()
        for stock_code in self.stock_list:
            # stock code format: SH600000
            print(f"{time.ctime()}: Recording interest of {stock_code}.")
            try:
                self._resolve_dividend(stock_code)
            except Exception as e:
                print(f"{time.ctime()}: Error - {e}")

    def _resolve_dividend(self, stock_code):
        # fetch data table
        _, url = read_json('URL_fh_163', CONF_FILE)
        url = url.format(stock_code[2:])
        content = requests.get(url, timeout=3)
        html = etree.HTML(content.text)
        table = html.xpath(
            "//table[@class='table_bg001 border_box limit_sale']")
        share_table = table[0].xpath(".//tr")
        table_name = f"{stock_code}_interest"
        dt = DataLine()
        # resolve the data table
        for line in share_table:
            data_line = line.xpath(".//td/text()")
            if len(data_line) > 6:
                data_key, sql = dt.resolve(data_line, table_name)
                query = (f"SELECT * from {table_name} where "
                         f"report_date='{data_key}'")
                result = self.mysql.session.execute(query).fetchall()
                if not result:
                    self.mysql.session.execute(sql)
                    self.mysql.session.commit()


class codeFormat(object):
    def __call__(self, stock_code):
        if type(stock_code) == str:
            stock_code = stock_code.upper()
            if re.match(r'^[A-Z][A-Z]\d{6}', stock_code):
                # format <SH600000> or <SZ000001>
                pass
            elif re.match(r'(\d{6}).([A-Z][A-Z])\Z', stock_code):
                # format <600000.SH> or <0000001.SZ>
                result = re.match(r'(\d{6}).([A-Z][A-Z]\Z)', stock_code)
                stock_code = result.group(2)+result.group(1)
            else:
                stock_code = None
            return stock_code

    def net_ease_code(self, stock_code):
        stock_code = self.__call__(stock_code)
        if type(stock_code) == str:
            if stock_code[:2] == 'SH':
                stock_code = '0' + stock_code[2:]
            elif stock_code[:2] == 'SZ':
                stock_code = '1' + stock_code[2:]
            else:
                stock_code = None
        else:
            stock_code = None
        return stock_code


def create_stock_list(flag='all'):
    # Shanghai A : sha
    # Shenzhen A : sza
    # Chuangyeban : cyb
    # Zhongxiaoban : zxb
    # Shanghai index : shi
    # Shenzhen index : szi
    # Hongkong stock : hk
    indices = []
    sha = ['SH600000']*4000
    for i in range(len(sha)):
        sha[i] = 'SH' + '60' + str(i).zfill(4)
    sza = ['SZ000001']*1000
    for i in range(len(sza)):
        sza[i] = 'SZ' + str(i).zfill(6)
    cyb = ['SZ300001']*1000
    for i in range(len(cyb)):
        cyb[i] = 'SZ' + '300' + str(i).zfill(3)
    zxb = ['SZ002000']*1000
    for i in range(len(zxb)):
        zxb[i] = 'SZ' + '002' + str(i).zfill(3)
    shb = ['SH900000']*4000
    for i in range(len(shb)):
        shb[i] = 'SH' + '900' + str(i).zfill(3)
    szb = ['SZ200001']*1000
    for i in range(len(szb)):
        szb[i] = 'SZ' + '200' + str(i).zfill(3)
    shi = ['SH000000']*2000
    for i in range(999):
        shi[i] = 'SH' + str(i).zfill(6)
        shi[i + 1000] = 'SH' + '950' + str(i).zfill(3)
    szi = ['SZ399000']*1000
    for i in range(len(szi)):
        szi[i] = 'SZ' + '399' + str(i).zfill(3)
    kcb = ['SH688001']*1000
    for i in range(len(kcb)):
        kcb[i] = 'SH' + '688' + str(i).zfill(3)
    hk = ['HK00001']*10000
    for i in range(len(hk)):
        hk[i] = 'HK'+str(i+1).zfill(5)

    if flag == 'all':
        indices.extend(sha)
        indices.extend(sza)
        indices.extend(cyb)
        indices.extend(zxb)
        indices.extend(szb)
        indices.extend(shi)
        indices.extend(szi)
        indices.extend(kcb)
    elif flag == 'stocks':
        indices.extend(sha)
        indices.extend(sza)
    elif flag == 'a':
        indices.extend(sha)
        indices.extend(sza)
    elif flag == 'b':
        indices.extend(shb)
        indices.extend(szb)
    elif flag == 'zxb':
        indices.extend(zxb)
    elif flag == 'cyb':
        indices.extend(cyb)
    elif flag == 'hk':
        indices.extend(hk)
    else:
        pass
    return indices


def random_header():
    return 1


def str2zero(input_str, return_type='i'):
    if input_str != '--':
        return input_str
    else:
        if return_type == 'i':
            return 'NULL'
        else:
            return 'NULL'


class DataLine(object):

    # Resolve the dataline
    # and convert it into sql.

    def __init__(self):
        self.report_date = datetime.now()
        self.record_date = datetime.now()
        self.xrdr_date = datetime.now()
        self.share_date = None
        self.year = datetime.now().timetuple()[0]
        self.bonus = 0.0
        self.increase = 0.0
        self.dividend = 0.0
        self.time = datetime.now().timetuple()

    def resolve(self, data_line, table_name):
        self.report_date = datetime.strptime(
            data_line[0], TIME_FMT)
        self.year = int(data_line[1])
        self.bonus = float(str2zero(data_line[4]))
        self.increase = float(str2zero(data_line[3]))
        self.dividend = float(str2zero(data_line[2]))
        self.record_date = datetime.strptime(
            data_line[5], TIME_FMT)
        self.xrdr_date = datetime.strptime(
            data_line[6], TIME_FMT)
        self.share_date = datetime.strptime(
            data_line[7],
            TIME_FMT) if data_line[7] != '--' else None
        if self.share_date:
            sql = (f"INSERT INTO {table_name}"
                   "(report_date, year, bonus, increase,"
                   "dividend, record_date, xrdr_date,"
                   "share_date)"
                   f"VALUES ('{self.report_date}',"
                   f"{self.year}, {self.bonus},{self.increase},"
                   f"{self.dividend},'{self.record_date}',"
                   f"'{self.xrdr_date}','{self.share_date}')")
        else:
            sql = (f"INSERT INTO {table_name}"
                   "(report_date, year, bonus, increase,"
                   "dividend, record_date, xrdr_date)"
                   f"VALUES ('{self.report_date}',"
                   f"{self.year}, {self.bonus},{self.increase},"
                   f"{self.dividend},'{self.record_date}',"
                   f"'{self.xrdr_date}')")
        return self.report_date, sql

    def __repr__(self):
        return str(self.year)


def event_stock_flag():
    header = mysqlHeader('root', '6414939', 'stock')
    mysql = mysqlBase(header)
    stock_list = fetch_no_flag_stock()
    df = pd.DataFrame(stock_list, columns=['stock_code'])
    df['flag'] = None
    print(df.head(5))
    for i in range(df.shape[0]):
        if re.match(r'^SH0', df.loc[i, 'stock_code']):
            df.loc[i, 'flag'] = 'index'
            print(df.iloc[i].values)
            sql = f"update stock_list set flag=\
                   '{df.loc[i,'flag']}' where stock_code=\
                    '{df.loc[i,'stock_code']}'"
            mysql.session.execute(sql)
            mysql.session.commit()
        elif re.match(r'^SH6', df.loc[i, 'stock_code']):
            df.loc[i, 'flag'] = 'stock'
            sql = f"update stock_list set flag=\
                   '{df.loc[i,'flag']}' where stock_code=\
                    '{df.loc[i,'stock_code']}'"
            mysql.session.execute(sql)
            mysql.session.commit()
        elif re.match(r'^SZ0', df.loc[i, 'stock_code']):
            df.loc[i, 'flag'] = 'stock'
            sql = f"update stock_list set flag=\
                   '{df.loc[i,'flag']}' where stock_code=\
                    '{df.loc[i,'stock_code']}'"
            mysql.session.execute(sql)
            mysql.session.commit()
        elif re.match(r'^SZ3', df.loc[i, 'stock_code']):
            df.loc[i, 'flag'] = 'stock'
            sql = f"update stock_list set flag=\
                   '{df.loc[i,'flag']}' where stock_code=\
                    '{df.loc[i,'stock_code']}'"
            mysql.session.execute(sql)
            mysql.session.commit()


class EventRehabilitation(StockEventBase):
    def rehabilitate(self, stock_code):
        """
        Main function, rehabilitation process.
        """
        try:
            # fetching data from mysql.
            sql = (
                "select trade_date,open_price,close_price,"
                "highest_price, lowest_price, prev_close_price,"
                f"amplitude from {stock_code}")
            result = self.mysql.session.execute(sql).fetchall()
            self.df = pd.DataFrame.from_dict(result)
            # data configging
            self._config_df()
            share = self._fetch_share(stock_code)
            self.df = pd.concat([self.df, share], axis=1, join='outer')
            # print(self.df.head(5))
            self.df.sort_index()
            self.df['reh'] = self.df['close']
            self.df.fillna(0, inplace=True)
            self.adjust_factor()
        except Exception:
            print(Exception)

    def adjust_factor(self):
        """
        Calculating adjust factor.
        Beta version.
        """
        self.df['factor'] = self.df['close']
        xr_flag = 0
        factor = 1.0
        for i in range(self.df.shape[0]):
            if i:
                if self.df.ix[i, 'dividend']+self.df.ix[i, 'bonus']+self.df.ix[i, 'increase']:
                    xr_flag = 2
                    factor = factor*self.df.ix[i-1, 'close']/self.df.ix[i, 'prev_close']
                else:
                    if xr_flag:
                        xr_flag -= 1
            self.df.ix[i, 'factor'] = factor
            self.df.ix[i, 'reh'] = self.df.ix[i, 'close']*factor
            if xr_flag:
                pass
                # print(
                #    self.df.index.T[i], self.df.ix[i, 'close'], self.df.ix[i, 'reh'], self.df.ix[i, 'factor'],
                #    self.df.ix[i, 'dividend'], self.df.ix[i, 'bonus'], self.df.ix[i, 'increase'])

    def _config_df(self):
        """
        Config dataframe, set data type, column index, etc.
        """
        # setting column index.
        self.df.columns = ['date', 'open', 'close', 'high', 'low', 'prev_close', 'amplitude']
        # setting data type.
        self.df['open'] = self.df['open'].astype(float)
        self.df['close'] = self.df['close'].astype(float)
        self.df['high'] = self.df['high'].astype(float)
        self.df['low'] = self.df['low'].astype(float)
        self.df['prev_close'] = self.df['prev_close'].astype(float)
        self.df['amplitude'] = self.df['amplitude'].astype(float)
        # convert date format from string to date.
        self.df = set_date_as_index(self.df)

    def _fetch_share(self, stock_code):
        """
        Getting interest data
        """
        # Querying data from mysql
        sql = (
            "SELECT xrdr_date, bonus, increase, dividend "
            f"FROM {stock_code}_interest")
        share = self.mysql.session.execute(sql).fetchall()
        # converting dict data to dataframe format
        share = pd.DataFrame.from_dict(share)
        # setting column index
        share.columns = ['date', 'bonus', 'increase', 'dividend']
        # converting data format and setting index
        share = set_date_as_index(share)
        return share

    def update_adjust_factor(self, stock_code):
        # first judge whether adjust factor has been calculated.
        for index, row in self.df.iterrows():
            # print(type(index), row['factor'])
            try:
                sql = (
                    f"update {stock_code} set trade_date='{index}',"
                    f"adjust_factor={row['factor']} "
                    f"where trade_date='{index}'")
                self.mysql.engine.execute(sql)
            except Exception as e:
                print(
                    ADJUST_FACTOR_ERROR.format(
                        code=stock_code,
                        trade_date=index,
                        factor=row['factor']))


class EventTradeDetail(StockEventBase):
    def fetch_trade_detail_data(self, stock_code, trade_date):
        year = '2019'
        # trade_date format: '20191118'
        code = self.coder.net_ease_code(stock_code)
        url = f"http://quotes.money.163.com/cjmx/{year}/{trade_date}/{code}.xls"
        df = pd.read_excel(url)
        filename = f"csv/{stock_code}_{trade_date}.csv"
        df.to_csv(filename, encoding='gb18030')


class EventFinanceReport(StockEventBase):
    def update_balance_sheet(self, stock_code):
        url = f"http://quotes.money.163.com/service/zcfzb_{stock_code[2:]}.html"
        df = self.fetch_balance_sheet(stock_code)
        update_period = '0'
        if df.empty is False:
            for index, row in df.iterrows():
                query_sql = (
                    f"SELECT * from balance_sheet_template where ("
                    f"report_period='{index}' and stock_code='{stock_code}')")
                # print(query_sql)
                result = self.mysql.engine.execute(query_sql).fetchall()
                # print(result)
                insert_sql = (
                    f"INSERT into balance_sheet_template (report_period, stock_code,"
                    "r1_assets,r2_current_assets,r3_fixed_assets,r4_current_liability,"
                    "r5_long_term_liability,r6_total_equity) "
                    f"VALUES ('{index}', '{stock_code}',{str2zero(row[51])},"
                    f"{str2zero(row[24])},{str2zero(row[50])},{str2zero(row[83])},"
                    f"{str2zero(row[92])},{str2zero(row[106])})")
                update_sql = (
                    f"UPDATE balance_sheet_template set "
                    f"r1_assets={str2zero(row[51])},r2_current_assets={str2zero(row[24])},"
                    f"r3_fixed_assets={str2zero(row[50])},r5_current_liability={str2zero(row[83])},"
                    f"r6_long_term_liability={str2zero(row[92])},r7_total_equity={str2zero(row[106])} "
                    f"WHERE (report_period='{index}' and stock_code='{stock_code}')"
                )
                if index > update_period:
                    update_period = index
                    # print(update_period)
                if result:
                    self.mysql.engine.execute(update_sql)
                else:
                    self.mysql.engine.execute(insert_sql)
            update_date_sql = (
                f"UPDATE stock_manager set gmt_balance='{update_period}' "
                f"WHERE stock_code='{stock_code}'")
            self.mysql.engine.execute(update_date_sql)

    def update_balance_sheet_asset(self, stock_code):
        url = f"http://quotes.money.163.com/service/zcfzb_{stock_code[2:]}.html"
        df = self.fetch_balance_sheet(stock_code)
        update_period = '0'
        if df.empty is False:
            for index, row in df.iterrows():
                update_sql = (
                    f"UPDATE balance_sheet_template set "
                    f"r1_1_bank_and_cash={str2zero(row[0])},r1_3_inventory={str2zero(row[19])},"
                    f"r3_1_fixed_assets={str2zero(row[36])},r3_2_goodwill={str2zero(row[45])} "
                    f"WHERE (report_period='{index}' and stock_code='{stock_code}')"
                )
                if index > update_period:
                    update_period = index
                    # print(update_period)
                self.mysql.engine.execute(update_sql)

    def fetch_balance_sheet(self, stock_code):
        """
        read csv data and return a dataframe object.
        """
        # config file is a url file.
        # _, url = read_json('URL_163_MONEY', CONF_FILE)
        url = f"http://quotes.money.163.com/service/zcfzb_{stock_code[2:]}.html"
        df = pd.read_csv(url, encoding='gb18030')
        if df.empty is False:
            df = df.T
            result = df.ix[1:-1, :]
        else:
            result = df
        return result


def set_date_as_index(df):
    df['date'] = pd.to_datetime(df['date'], format=TIME_FMT)
    df.set_index('date', inplace=True)
    # exception 1, date index not exists.
    # exception 2, date data is not the date format.
    return df


def sub_7_days_benefit_distribution():
    header = mysqlHeader('root', '6414939', 'stock')
    stock = mysqlBase(header)
    stock_list = stock.session.query(
        formStockList.stock_code).all()
    for s in stock_list:
        try:
            stock_code = s[0]
            sql = f"select trade_date,close_price from {stock_code}"
            result = stock_con.session.execute(sql).fetchall()
            x = pd.DataFrame.from_dict(result)
            x.columns = ['trade_date', 'close_price']
            li = []
            k = 0
            while k < 300:
                i = random.randint(0, x.shape[0]-10)
                benefit = (x.iloc[i+7, 1]-x.iloc[i, 1])/x.iloc[i, 1]
                li.append(benefit)
                k = k+1

            y = pd.DataFrame.from_dict(l)
            print(f"{stock_code}: {y.mean()}, {y.std()}")
        except Exception as e:
            print(e)


def fetch_atr(stock_code):
    stock_conn = mysqlBase('root', '6414939', 'stock')
    sql = (
        f"select highest_price, lowest_price, "
        f"prev_close_price from {stock_code}")
    result = stock_conn.session.execute(sql).fetchall()
    result = pd.DataFrame.from_dict(result)
    result.columns = ['highest', 'lowest', 'prev_close']
    a1 = abs(result['highest']-result['lowest'])
    a2 = abs(result['prev_close']-result['highest'])
    a3 = abs(result['prev_close']-result['lowest'])
    atr = pd.DataFrame(list(zip(a1, a2, a3)))
    atr['max'] = atr.max(axis=1)
    print(atr.head(5))
    atr['ma14'] = pd.DataFrame.rolling(
        atr['max'], window=14, min_periods=14).mean()
    atr = atr[15:2700]
    print(atr)
    atr.plot()
    plt.show()
    return result


def test(stock_code):
    print(stock_code)
    stock_conn = MySQLBase('root', '6414939', 'stock')
    sql = f"select trade_date,open_price,close_price,\
            highest_price, lowest_price,\
            prev_close_price from {stock_code}"
    res = stock_conn.session.execute(sql).fetchall()
    res = pd.DataFrame.from_dict(res)
    res.columns = ['trade_date', 'open', 'close', 'high',
                   'low', 'prev_close']
    res['trade_date'] = pd.to_datetime(res['trade_date'])
    res.set_index('trade_date', inplace=True)
    res['up'] = ta.MAX(res['high'], timeperiod=20).shift(1)
    res['down'] = ta.MIN(res['low'], timeperiod=10).shift(1)
    res['ATR'] = ta.ATR(res['high'], res['low'],
                        res['close'], timeperiod=20)
    res['ret'] = res['close']/res['close'].shift(1)-1
    # res = res[30:100]
    # res = res.drop(['highest', 'lowest' ], axis=1)
    # res= res.drop(['ATR'],axis =1)
    x1 = res['high'] > res['up']
    x2 = res['high'].shift(1) < res['up'].shift(1)
    x = x1 & x2
    y1 = res['low'] < res['down']
    y2 = res['low'].shift(1) > res['down'].shift(1)
    y = y1 & y2
    res.loc[x, 'signal'] = 'B'
    res.loc[y, 'signal'] = 'S'
    # print(res.shape[0])
    buy_date = (res.loc[res['signal'] == 'B'].index).strftime("%Y-%m-%d")
    sell_date = (res.loc[res['signal'] == 'S'].index).strftime("%Y-%m-%d")
    # print(buy_date)
    # print(sell_date)
    buy_close = res[res['signal'] == 'B'].close.round(2).tolist()
    sell_close = res[res['signal'] == 'S'].close.round(2).tolist()
    # print(buy_close)
    # print(sell_close)
    # res.plot()
    # plt.show()
    # use pyecharts lib
    # res = res[30:400]
    # print(res.head(10))
    from mpl_finance import candlestick_ochl as kplot
    from matplotlib.dates import date2num
    from datetime import timedelta
    """
    fig, ax = plt.subplots()
    plt.xticks(rotation=45)
    plt.yticks()
    ax.xaxis_date()
    data_list = []
    for dt, row in res.iterrows():
        t = date2num(dt)
        op, cl, high, low = row[:4]
        # print(dt, row[:4])
        data = (t, op, cl, high, low)
        data_list.append(data)
    try:
        kplot(ax, data_list,
              width=1.0, colorup='r', colordown='green', alpha=0.75)
    except Exception as e:
        pass
        # print(e)
    # plt.show()
    """
    stock_conn.session.close()
    buy_index = res[res['close'] > res['down'].shift(1)].index
    # print(buy_index)
    res.loc[buy_index, 'close_signal'] = 1
    res['storage'] = res['close_signal'].shift(1)
    res['storage'].fillna(method='ffill', inplace=True)
    d = res[res['storage'] == 1].index[0]-timedelta(days=1)
    df1 = res.loc[d:].copy()
    df1['ret'][0] = 0
    df1['storage'][0] = 0
    df1['strategy_value'] = (
        df1['ret'].values*df1['storage'].values+1.0).cumprod()
    df1['index_value'] = (df1['ret'].values+1.0).cumprod()
    df1['sta_rate'] = df1['strategy_value']/df1['strategy_value'].shift(1)-1
    df1['index_rate'] = df1.ret
    total_ret = df1[['strategy_value', 'index_value']].iloc[-1]-1
    annual_ret = pow(1+total_ret, 250/len(df1))-1
    beta = df1[['sta_rate', 'index_rate']].cov().iat[0, 1] / \
        df1['index_rate'].var()
    alpha = (annual_ret['strategy_value']-annual_ret['index_value']*beta)
    exReturn = df1['sta_rate']-0.03/250
    import numpy as np
    sharp_ratio = np.sqrt(len(exReturn))*exReturn.mean()/exReturn.std()
    print('total ret:', total_ret.values[0])
    print('annual ret:', annual_ret.values[0])
    print('beta:', beta)
    print('alpha:', alpha)
    print('sharp ratio:', sharp_ratio)
    return (
        stock_code, total_ret.values[0], annual_ret.values[0],
        beta, alpha, sharp_ratio)


if __name__ == '__main__':
    header = mysqlHeader('root', '6414939', 'stock')
    stock = EventCreateStockTable()
