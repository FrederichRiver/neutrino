#!/usr/bin/python3
import pandas as pd
import requests
import random
from polaris.mysql8 import mysqlHeader, mysqlBase
from dev_global.env import GLOBAL_HEADER
from venus.stock_base import StockEventBase


class EventCompany(StockEventBase):
    def get_cooperation_info(self, stock_code):
        url = f"http://quotes.money.163.com/f10/gszl_{stock_code[2:]}.html#01f02"
        table = self.get_html_table(url, attr="[@class='table_bg001 border_box limit_sale table_details']")
        t = pd.read_html(table)[0]
        # print(t.iloc[12, 1])
        insert_sql = (
            "INSERT IGNORE INTO cooperation_info ("
            "stock_code, name, english_name, legal_representative, address,"
            "chairman, secratery, main_business, business_scope, introduction)"
            "VALUES ( "
            f"'{stock_code}','{t.iloc[2, 1]}','{t.iloc[3, 1]}',"
            f"'{t.iloc[6, 1]}','{t.iloc[1, 3]}','{t.iloc[4, 3]}','{t.iloc[5, 3]}',"
            f"'{t.iloc[10, 1]}','{t.iloc[11, 1]}','{t.iloc[12, 1]}')"
        )
        update_sql = (
            f"UPDATE cooperation_info set short_name='{t.iloc[1, 1]}',"
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


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    event = EventCompany(GLOBAL_HEADER)
    event.get_cooperation_info('SH601818')
