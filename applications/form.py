#!/usr/bin/python3
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base


__version__ = '1.0.8'


formTemplate = declarative_base()
formFinanceTemplate = declarative_base()
formInfomation = declarative_base()


class cooperation_info(formInfomation):
    __tablename__ = 'cooperation_info'
    # index = Column(Integer, nullable=False, autoincrement=True)
    name = Column(String(100))
    english_name = Column(String(100))
    stock_code = Column(String(10), primary_key=True)
    # type: 1,state enterprise; 2,
    type = Column(Integer)
    legal_representative = Column(String(20))
    address = Column(String(100))
    chairman = Column(String(20))
    secratery = Column(String(20))
    main_business = Column(String(100))
    business_scope = Column(String(1000))
    introduction = Column(String(1000))


class formFinanceInfo(formFinanceTemplate):
    __tablename__ = 'finance_info'
    stock_code = Column(String(10), primary_key=True)
    report_date = Column(Date, primary_key=True)
    roe = Column(Float)
    eps = Column(Float)
    pe = Column(Float)
    ttm = Column(Float)


class formInterest(formTemplate):
    # This is the template of stock interest.
    __tablename__ = 'template_stock_interest'
    report_date = Column(Date, primary_key=True)
    year = Column(Integer)
    bonus = Column(Float)
    increase = Column(Float)
    dividend = Column(Float)
    record_date = Column(Date)
    xrdr_date = Column(Date)
    share_date = Column(Date)


class formStockManager(formTemplate):
    __tablename__ = 'stock_manager'
    stock_code = Column(String(10), primary_key=True)
    stock_name = Column(String(20))
    gmt_create = Column(Date)
    gmt_modified = Column(Date)
    gmt_xrdr = Column(Date)
    gmt_balance = Column(Date)
    gmt_income = Column(Date)
    gmt_cashflow = Column(Date)
    flag = Column(String(10))

    def __str__(self):
        return None


class formStock(formTemplate):
    __tablename__ = 'template_stock'
    trade_date = Column(Date, primary_key=True)
    stock_name = Column(String(20))
    close_price = Column(Float)
    highest_price = Column(Float)
    lowest_price = Column(Float)
    open_price = Column(Float)
    prev_close_price = Column(Float)
    change_rate = Column(Float)
    amplitude = Column(Float)
    volume = Column(Integer)
    turnover = Column(Float)
    adjust_factor = Column(Float)

    def __str__(self):
        return "Form Stock List is a template."


class formFinance(formFinanceTemplate):
    __tablename__ = 'finance_factor'
    report_period = Column(Date, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    roe = Column(Float)
    pe = Column(Float)
    ttm = Column(Float)
    roic = Column(Float)
    croic = Column(Float)
    ebit = Column(Float)
    ebitda = Column(Float)
    noplat = Column(Float)
    # r5_quantity = Column(Float)


class formCashFlow(formFinanceTemplate):
    __tablename__ = 'cash_flow_sheet'
    report_period = Column(Date, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    r2_cash_received_from_sales_of_goods_or_rendering_services = Column(Float)
    r3_net_increase_in_customer_deposits_and_interbank_deposits = Column(Float)
    r13_refunds_of_taxes = Column(Float)
    r14_cash_received_relating_to_other_operating_activities = Column(Float)
    r15_subtotal_of_cash_inflows_in_operating_activities = Column(Float)
    r22_cash_paid_to_and_one_behalf_of_employees = Column(Float)
    r23_tax_payments = Column(Float)
    r24_cash_paid_relating_to_other_operating_activities = Column(Float)
    r27_cash_received_from_disposal_of_investments = Column(Float)


class formBalanceSheet(formFinanceTemplate):
    __tablename__ = 'balance_sheet_template'
    report_period = Column(Date, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    r1_assets = Column(Float)
    r2_current_assets = Column(Float)
    r3_non_current_assets = Column(Float)
    # r4_liability = Column(Float)
    r4_current_liability = Column(Float)
    r5_long_term_liability = Column(Float)
    r6_total_equity = Column(Float)
    r1_1_bank_and_cash = Column(Float)
    r1_2_current_investment = Column(Float)
    r1_3_inventory = Column(Float)
    r1_3_less_provision_for_inventory = Column(Float)
    r3_1_fixed_assets = Column(Float)
    r3_2_goodwill = Column(Float)
    r5_1_short_term_loans = Column(Float)
    r5_2_notes_payable = Column(Float)
    r5_3_accounts_payable = Column(Float)
    r6_1_long_term_loans = Column(Float)


class formIncomeStatement(formFinanceTemplate):
    __tablename__ = 'income_statement_template'
    report_period = Column(Date, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    r1_total_revenue = Column(Float)
    r2_total_cost = Column(Float)
    r3_profit_from_operation = Column(Float)
    r4_net_profit = Column(Float)
    r1_1_revenue = Column(Float)
    r1_2_interest_income = Column(Float)
    r1_3_other_operating_income = Column(Float)
    r2_1_operating_cost = Column(Float)
    r2_2_rd_expense = Column(Float)
    r2_3_ga_expense = Column(Float)
    r2_4_selling_expense = Column(Float)
    r2_5_finance_expense = Column(Float)
    r3_1_non_operating_income = Column(Float)
    r3_2_non_operating_expense = Column(Float)
    r3_3_disposal_loss_on_non_current_asset = Column(Float)
    r3_4_profit_before_tax = Column(Float)
    r3_5_income_tax = Column(Float)
    r3_6_unrealized_investment_loss = Column(Float)


"""
class formBalanceSheet(formFinanceTemplate):
    __tablename__ = 'balance_sheet_template'
    report_period = Column(Date, primary_key=True)
    r1_assets = Column(Float)
    r2_current_assets = Column(Float)
    r3_bank_and_cash = Column(Float)
    r4_current_investment = Column(Float)
    r5_entrusted_loan_receivable_due_within_one_year = Column(Float)
    r6_less_impairment_entrusted_loan_receivable_due_within_one_year = Column(Float)
    r7_net_bal_of_current_investment = Column(Float)
    r8_notes_receivable = Column(Float)
    r9_dividend_receivable = Column(Float)
    r10_interest_receivable = Column(Float)
    r11_account_receivable = Column(Float)
    r12_less_bad_debt_provision_for_account_receivable = Column(Float)
    r13_net_bal_of_current_receivable = Column(Float)
    r14_other_receivable = Column(Float)
    r15_less_bad_debt_provision_for_other_receivable = Column(Float)
    r16_net_bal_of_other_receivable = Column(Float)
    r17_prepayment = Column(Float)
    r18_subsidy_receivable = Column(Float)
    r19_inventory = Column(Float)
    r20_less_provision_for_inventory = Column(Float)
    r21_net_bal_of_inventory = Column(Float)
    r22_amount_due_from_customer_for_contract_work = Column(Float)
    r23_deferred_expense = Column(Float)
    r24_long_term_debt_investment_due_within_one_year = Column(Float)
    r25_finance_lease_receivables_due_within_one_year = Column(Float)
    r26_other_current_assets = Column(Float)
    r27_total_current_assets = Column(Float)
    r28_long_term_investment = Column(Float)
    r29_long_term_equity_investment = Column(Float)
    r30_entrusted_loan_receivable = Column(Float)
    r31_long_term_debt_investment = Column(Float)
    r32_total_for_long_term_investment = Column(Float)


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
"""

if __name__ == '__main__':
    stocklist = formStockList()
    print(stocklist)
