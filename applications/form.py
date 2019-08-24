#!/usr/bin/python3
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base

formTemplate = declarative_base()
formBase = declarative_base()
formReportBase = declarative_base()


class formInterest(formTemplate):
    # This is the template of stock interest.
    __tablename__ = 'template_stock_interest'
    report_date = Column(Date, primary_key=True)
    year = Column(Integer)
    bonus = Column(Float(precision=8,
                         decimal_return_scale=3))
    increase = Column(Float(precision=8,
                            decimal_return_scale=3))
    dividend = Column(Float(precision=8,
                            decimal_return_scale=3))
    record_date = Column(Date)
    xrdr_date = Column(Date)
    share_date = Column(Date)


class formStockList(formTemplate):
    __tablename__ = 'stock_list'
    stock_code = Column(String(10), primary_key=True)
    stock_name = Column(String(10))
    gmt_create = Column(Date)
    gmt_modified = Column(Date)
    flag = Column(String(10))

    def __repr__(self):
        # Not tested.
        return (f"Stock<{self.stock_code},{self.tock_name}>"
                "is created at {gmt_create}"
                "and modified at {gmt_modified}")


class formStock(formTemplate):
    __tablename__ = 'template_stock'
    trade_date = Column(Date, primary_key=True)
    stock_name = Column(String(10))
    close_price = Column(Float(precision=10,
                               decimal_return_scale=3))
    highest_price = Column(Float(precision=10,
                                 decimal_return_scale=3))
    lowest_price = Column(Float(precision=10,
                                decimal_return_scale=3))
    open_price = Column(Float(precision=10,
                              decimal_return_scale=3))
    prev_close_price = Column(Float(precision=10,
                                    decimal_return_scale=3))
    change_rate = Column(Float(precision=5,
                               decimal_return_scale=3))
    amplitude = Column(Float(precision=5,
                             decimal_return_scale=3))
    volume = Column(Integer)
    turnover = Column(Float)


class formFinanceReport(formBase):
    __tablename__ = 'finance_report'
    name = Column(String(10), primary_key=True)

    def __repr__(self):
        pass


class formCurrencyFlow(formReportBase):
    __tablename__ = 'currency_flow_report'
    report_date = Column(Date, primary_key=True)
    r2_cash_received_from_sales_of_goods_or_rendering_services = Column(Float)
    r3_net_increase_in_customer_deposits_and_interbank_deposits = Column(Float)
    r13_refunds_of_taxes = Column(Float)
    r14_cash_received_relating_to_other_operating_activities = Column(Float)
    r15_subtotal_of_cash_inflows_in_operating_activities = Column(Float)
    r22_cash_paid_to_and_one_behalf_of_employees = Column(Float)
    r23_tax_payments = Column(Float)
    r24_cash_paid_relating_to_other_operating_activities = Column(Float)
    r27_cash_received_from_disposal_of_investments = Column(Float)


if __name__ == '__main__':
    from libmysql8 import MySQLBase, createTable
    import pandas as pd
    import json
    from sqlalchemy.engine.url import URL as engine_url
    from sqlalchemy import create_engine, MetaData
    """
    test = MySQLBase('root', '6414939', 'test')
    createTable(formReport, test.engine)
    url = 'http://quotes.money.163.com/service/xjllb_{0}.html'
    url = url.format('600795')
    r = pd.read_csv(url,
                    header=None,
                    encoding='gb18030')
    r = r.drop(columns=[0])
    result = pd.DataFrame(r.T, columns=r.index)
    with open('./config/column_config.json', 'r') as js:
        load_dist = json.load(js)

    column_list = list(load_dist.values())

    result.columns = column_list
    result.set_index('c1_report_date', inplace=True)
    # print(result.head(5))
    lst = query_stock_list
    print(lst)
    """
