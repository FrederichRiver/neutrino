#!/usr/bin/python3
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base


__version__ = '1.0.3'


formTemplate = declarative_base()
formFinanceTemplate = declarative_base()


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
    stock_name = Column(String(20))
    gmt_create = Column(Date)
    gmt_modified = Column(Date)
    gmt_xrdr = Column(Date)
    flag = Column(String(10))

    def __str__(self):
        # Not tested.
        return (f"Stock<{self.stock_code},{self.stock_name}>"
                "is created at {gmt_create}"
                "and modified at {gmt_modified}")


class formStock(formTemplate):
    __tablename__ = 'template_stock'
    trade_date = Column(Date, primary_key=True)
    stock_name = Column(String(20))
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
    back_adjust_factor = Column(Float)

    def __str__(self):
        return "Form Stock List is a template."


class formFinanceReport(formFinanceTemplate):
    __tablename__ = 'finance_report'
    name = Column(String(10), primary_key=True)

    def __str__(self):
        pass


class formCurrencyFlow(formFinanceTemplate):
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
    stocklist = formStockList()
    print(stocklist)
