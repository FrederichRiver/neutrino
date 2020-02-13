#!/usr/bin/python3
import pandas as pd
import numpy as np
from dev_global.env import CONF_FILE, TIME_FMT
from jupiter.utils import read_url, ERROR, drop_space, INFO
from venus.stock_base import StockEventBase
from sqlalchemy.types import Date, DECIMAL, Integer, NVARCHAR
from venus.form import formStockManager


class EventTradeDataManager(StockEventBase):
    """
    It is a basic event, which fetch trade data and manage it.
    """
    # def __init__(self):
    #    super(StockEventBase, self).__init__()
    def url_netease(self, stock_code, start_date, end_date):
        url = read_url('URL_163_MONEY', CONF_FILE)
        query_code = self.coder.net_ease_code(stock_code)
        netease_url = url.format(query_code, start_date, end_date)
        return netease_url

    def get_trade_data(self, stock_code, end_date, start_date='19901219'):
        """
        read csv data and return dataframe type data.
        """
        # config file is a url file.
        url = self.url_netease(stock_code, start_date, end_date)
        result = pd.read_csv(url, encoding='gb18030')
        return result

    def get_stock_name(self, stock_code):
        """
        Searching stock name from net ease.
        """
        try:
            result = self.get_trade_data(stock_code)
            if not result.empty:
                stock_name = drop_space(result.iloc[1, 2])
            else:
                stock_name = None
        except Exception as e:
            ERROR(f"Failed when fetching stock name of {stock_code}.")
            ERROR(e)
            stock_name = None
        return stock_code, stock_name

    def record_stock(self, stock_code):
        """
        Record table <stock_code> into database.
        """
        result = self.check_stock(stock_code)
        # if table exists, result = (stock_code,)
        # else result = (,)
        if not result:
            self.create_stock_table(stock_code)

    def check_stock(self, stock_code):
        """
        Check whether table <stock_code> exists.
        """
        result = self.mysql.select_one(
            stock_code, 'stock_code', f"stock_code='{stock_code}'")
        return result

    def create_stock_table(self, stock_code):
        _, stock_name = self.get_stock_name(stock_code)
        if stock_name:
            stock_orm = formStockManager(
                stock_code=stock_code,
                stock_name=stock_name,
                gmt_create=self.Today()
                )
            self.mysql.session.add(stock_orm)
            self.mysql.session.commit()
            self.mysql.create_table_from_table(
                stock_code, 'template_stock')
            INFO(f"Create table {stock_code}.")

    def data_cleaning(self, df):
        """
        df is a DataFrame like data.
        """
        df.drop(['stock_code'], axis=1, inplace=True)
        df.replace('None', np.nan, inplace=True)
        df = df.dropna(axis=0, how='any')
        return df

    def init_stock_data(self, stock_code):
        """
        used when first time download stock data.
        """
        result = self.get_trade_data(stock_code)
        result.columns = ['trade_date', 'stock_code',
                          'stock_name', 'close_price',
                          'highest_price', 'lowest_price',
                          'open_price', 'prev_close_price',
                          'change_rate', 'amplitude',
                          'volume', 'turnover']
        result = self.data_cleaning(result)
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
        # stk = formStockManager(stock_code=stock_code,
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
                formStockManager.stock_code,
                formStockManager.gmt_modified
            ).filter_by(stock_code=stock_code)
            if query:
                query.update(
                    {"gmt_modified": self.Today()})
            self.mysql.session.commit()
        except Exception as e:
            ERROR(f"Problem when initially download {stock_code} data.")

    def download_stock_data(self, stock_code):
        # print(stock_code)
        result = self.get_trade_data(stock_code, self.today)
        result.columns = ['trade_date', 'stock_code',
                          'stock_name', 'close_price',
                          'highest_price', 'lowest_price',
                          'open_price', 'prev_close_price',
                          'change_rate', 'amplitude',
                          'volume', 'turnover']
        result = self.data_cleaning(result)
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
        # stk = formStockManager(stock_code=stock_code,
        #            gmt_modified=datetime.today())
        # engine.session.add(stk)
        # engine.session.commit()
        from datetime import date
        try:
            query = self.mysql.select_values(stock_code, 'trade_date')
            sql = f"SELECT trade_date from {stock_code}"
            query = self.mysql.engine.execute(sql).fetchall()
            # t2 = result[-1][0]
            result['trade_date'] = pd.to_datetime(result['trade_date'], format=TIME_FMT)
            result = result.sort_values('trade_date')
            # print(result.head(5))
            t2 = query[-1][0]
            update_date = t2
            for index, row in result.iterrows():
                t1 = row['trade_date'].to_pydatetime().date()
                if t1 > t2:
                    insert_sql = (
                        f"INSERT into {stock_code} "
                        "(trade_date,stock_name,close_price,"
                        "highest_price,lowest_price,open_price,prev_close_price,"
                        "change_rate,amplitude,volume,turnover)"
                        f"VALUES('{row['trade_date']}','{row['stock_name']}',"
                        f"{row['close_price']},{row['highest_price']},"
                        f"{row['lowest_price']},{row['open_price']},"
                        f"{row['prev_close_price']},{row['change_rate']},"
                        f"{row['amplitude']},{row['volume']},{row['turnover']})"
                        )
                    self.mysql.engine.execute(insert_sql)
                    update_date = t1
            query = self.mysql.session.query(
                        formStockManager.stock_code,
                        formStockManager.gmt_modified
                    ).filter_by(stock_code=stock_code)
            if query:
                query.update(
                    {"gmt_modified": update_date})
            self.mysql.session.commit()
        except Exception as e:
            ERROR(f"Failed when donwload {stock_code} data.")
            ERROR(e)

    def get_trade_detail_data(self, stock_code, trade_date):
        # trade_date format: '20191118'
        code = self.coder.net_ease_code(stock_code)
        url = read_url("URL_tick_data", CONF_FILE).format(
            trade_date[:4], trade_date, code)
        try:
            df = pd.read_excel(url)
            csv_path = "/home/friederich/Documents/dev/neutrino/csv/"
            filename = csv_path + f"{stock_code}_{trade_date}.csv"
            df.to_csv(filename, encoding='gb18030')
        except Exception as e:
            ERROR(f"Failed when download {stock_code} tick data.")
            ERROR(e)


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    event = EventTradeDataManager(GLOBAL_HEADER)
    stock_list = event.get_all_stock_list()
    stock_code = 'SH601818'
    # for stock_code in stock_list:
    event.download_stock_data(stock_code)
