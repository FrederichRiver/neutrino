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
    adjust_factor = Column(Float)

    def __str__(self):
        return "Form Stock List is a template."


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


class formFinanceReport(formFinanceTemplate):
    __tablename__ = 'income_statement2'
    report_period = Column(Date, primary_key=True)
    r1_revenue = Column(Float, comment='revenue')
    r2_total_operating_cost = Column(Float)
    r3_operating_profit = Column(Float)
    r4_net_profit = Column(Float)
    r5_current_asset = Column(Float)
    r6_long_term_asset = Column(Float)
    r7_current_liability = Column(Float)
    r8_long_term_liability = Column(Float)


class formFinanceSummary(formFinanceTemplate):
    __tablename__ = 'summary'
    report_period = Column(Date, primary_key=True)
    r1_revenue = Column(Float)
    r2_gross_profit = Column(Float)
    r3_profit_from_operating = Column(Float)
    r4_net_profit = Column(Float)
    r5_total_asset = Column(Float)
    r6_total_liability = Column(Float)
    r7_roe = Column(Float)


class formCashFlow(formFinanceTemplate):
    __tablename__ = 'cash_flow'
    report_period = Column(Date, primary_key=True)


class formAssetLiability(formFinanceTemplate):
    __tablename__ = 'asset'
    report_period = Column(Date, primary_key=True)


class formIncomeStatement(formFinanceTemplate):
    __tablename__ = 'income_statement'
    report_period = Column(Date, primary_key=True)
    r1_revenue = Column(Float)
    r2_less_cost_of_sales = Column(Float)
    r3_sales_tax = Column(Float)
    r4_gross_profit = Column(Float)
    r5_add_other_operating_income = Column(Float)
    r6_less_other_operating_expense = Column(Float)
    r7_less_selling_and_distribution_expense = Column(Float)
    r8_g_a_expense = Column(Float)
    r9_finance_expense = Column(Float)
    r10_profit_from_operation = Column(Float)
    r11_add_investment_income = Column(Float)
    r12_subsidy_income = Column(Float)
    r13_non_operating_income = Column(Float)
    r14_less_non_operating_expense = Column(Float)
    r15_profit_before_tax = Column(Float)
    r16_less_income_tax = Column(Float)
    r17_minority_interest = Column(Float)
    r18_add_unrealised_investment_losses = Column(Float)
    r19_net_profit = Column(Float)
    r20_add_retained_profit = Column(Float)
    r21_other_transfer_in = Column(Float)
    r22_profit_available_for_distribution = Column(Float)
    r23_less_appropriation_of_statutory_surplus_reserves = Column(Float)
    r24_appropriation_of_statutory_welfare_fund = Column(Float)
    r25_appropriation_of_staff_incentive_and_welfare_fund = Column(Float)
    r26_appropriation_of_reserve_fund = Column(Float)
    r27_appropriation_of_enterprise_expansion_fund = Column(Float)
    r28_captial_redemption = Column(Float)
    r29_profit_avaliable_for_owners_distribution = Column(Float)
    r30_less_appropriation_of_preference_share_dividend = Column(Float)
    r31_appropriation_of_discretionary_surplus_reserve = Column(Float)
    r32_appropriation_of_ordinary_share_dividend = Column(Float)
    r33_transfer_from_ordinary_share_dividend_to_paid_in_capital = Column(Float)
    r34_retained_profit_after_appropriation = Column(Float)
    r35_supplementary_infomation = Column(Float)


if __name__ == '__main__':
    stocklist = formStockList()
    print(stocklist)
