#!/usr/bin/python3
from venus.stock_base import StockEventBase
from venus.form import formInterest
from jupiter.utils import ERROR


class EventCreateInterestTable(StockEventBase):
    def create_interest_table(self):
        from form import formInterest
        create_table_from_table(
                "stock_interest",
                formInterest.__tablename__,
                self.mysql.engine)

    def record_interest(self):
        self.fetch_all_stock_list()
        for stock_code in self.stock_list:
            # stock code format: SH600000
            try:
                self._resolve_dividend(stock_code)
            except Exception:
                ERROR(f"Error while recording interest of {stock_code}")

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
