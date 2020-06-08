#!/usr/bin/python3
import pandas as pd
import re
import pandas
import requests
import random
from polaris.mysql8 import mysqlHeader, mysqlBase
from dev_global.env import GLOBAL_HEADER
from venus.stock_base import StockEventBase


class EventCompany(StockEventBase):
    def record_company_infomation(self, stock_code):
        url = f"http://quotes.money.163.com/f10/gszl_{stock_code[2:]}.html#01f02"
        table = self.get_html_table(url, attr="[@class='table_bg001 border_box limit_sale table_details']")
        t = pd.read_html(table)[0]
        # print(t.iloc[12, 1])
        insert_sql = (
            "INSERT IGNORE INTO company_infomation ("
            "stock_code, company_name, english_name, legal_representative, address,"
            "chairman, secratery, main_business, business_scope, introduction) "
            "VALUES ( "
            f"'{stock_code}','{t.iloc[2, 1]}','{t.iloc[3, 1]}',"
            f"'{t.iloc[6, 1]}','{t.iloc[1, 3]}','{t.iloc[4, 3]}','{t.iloc[5, 3]}',"
            f"'{t.iloc[10, 1]}','{t.iloc[11, 1]}','{t.iloc[12, 1]}')"
        )
        try:
            self.mysql.engine.execute(insert_sql)
        except Exception as e:
            print(e)
        
    def get_cooperation_info(self, stock_code):
        url = f"http://quotes.money.163.com/f10/gszl_{stock_code[2:]}.html#01f02"
        table = self.get_html_table(url, attr="[@class='table_bg001 border_box limit_sale table_details']")
        t = pd.read_html(table)[0]
        # print(t.iloc[12, 1])
        insert_sql = (
            "INSERT IGNORE INTO company_infomation ("
            "stock_code, company_name, english_name, legal_representative, address,"
            "chairman, secratery, main_business, business_scope, introduction)"
            "VALUES ( "
            f"'{stock_code}','{t.iloc[2, 1]}','{t.iloc[3, 1]}',"
            f"'{t.iloc[6, 1]}','{t.iloc[1, 3]}','{t.iloc[4, 3]}','{t.iloc[5, 3]}',"
            f"'{t.iloc[10, 1]}','{t.iloc[11, 1]}','{t.iloc[12, 1]}')"
        )
        update_sql = (
            f"UPDATE company_infomation set short_name='{t.iloc[1, 1]}',"
            f"name='{t.iloc[2, 1]}', english_name='{t.iloc[3, 1]}',"
            f"legal_representative='{t.iloc[6, 1]}', address='{t.iloc[1, 3]}',"
            f"chairman='{t.iloc[4, 3]}', secratery='{t.iloc[5, 3]}',"
            f"main_business='{t.iloc[10, 1]}', business_scope='{t.iloc[11, 1]}',"
            f"introduction='{t.iloc[12, 1]}' "
            f"WHERE stock_code='{stock_code}'"
            )
        try:
            self.mysql.engine.execute(insert_sql)
        except Exception:
            self.mysql.engine.execute(update_sql)

    def record_stock_structure(self, stock_code):
        import requests
        from lxml import etree
        url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/{stock_code[2:]}/stocktype/TotalStock.phtml"
        table = self.get_html_table(url, attr="[@id='historyTable07']")
        df = self._resolve_stock_structure_table(table)
        self._update_stock_structure(stock_code, df)


    def _resolve_stock_structure_table(self, table) -> pandas.DataFrame:
        df = pd.read_html(table)
        if df:
            df[0].columns = ['change_date', 'total_stock']
            result = df[0]
            result['total_stock'] = df[0]['total_stock'].apply(filter_str2float)
            result['change_date'] = pandas.to_datetime(result['change_date'])
            return result
        else:
            return pandas.DataFrame()

    def _update_stock_structure(self, stock_code, df:pandas.DataFrame):
        TAB_COMP_STOCK_STRUC = 'company_stock_structure'
        value = {}
        if not df.empty:
            for index, row in df.iterrows():
                sql = (
                    f"INSERT IGNORE into {TAB_COMP_STOCK_STRUC} ("
                    f"stock_code,report_date,total_stock) "
                    f"VALUES ('{stock_code}','{row['change_date']}',{row['total_stock']})")
                self.mysql.engine.execute(sql)

def filter_str2float(x):
    result = re.match(r'(\d+)', x)
    if result:
        return 10000 * float(result[1])
    else:
        return 0

if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    event = EventCompany(GLOBAL_HEADER)
    event.record_stock_structure('SH601818')