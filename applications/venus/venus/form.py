#!/usr/bin/python3
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base


__version__ = '1.0.11'


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


class formInterest(formTemplate):
    # This is the template of stock interest.
    __tablename__ = 'template_stock_interest'
    report_date = Column(Date, primary_key=True)
    char_stock_code = Column(String(10), primary_key=True)
    int_year = Column(Integer)
    float_bonus = Column(Float)
    float_increase = Column(Float)
    float_dividend = Column(Float)
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
        return "<Stock Manager>"


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
        return "<Stock template>"


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


class formCashFlow(formFinanceTemplate):
    __tablename__ = 'cash_flow_sheet'
    report_period = Column(Date, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    r1_cash_flow_from_operating_activities = Column(Float)
    r2_cash_flow_from_investment = Column(Float)
    r3_cash_flow_from_finance_activities = Column(Float)
    r4_effect_of_foriegn_exchange_rate_changes_on_cash_effect = Column(Float)
    r5_net_increase_in_cash_and_cash_equivalent = Column(Float)
    r1_1_cash_received_from_sales_of_goods_or_rendering_services = Column(Float)
    r1_2_subtotal_of_cash_inflow_from_operating = Column(Float)
    r1_3_subtotal_of_cash_outflow_from_operating = Column(Float)
    r1_4_captial_expenditure = Column(Float)
    r2_1_subtotal_of_cash_inflow_from_investment = Column(Float)
    r2_2_subtotal_of_cash_outflow_from_investment = Column(Float)
    r3_1_subtotal_of_cash_inflow_from_finance = Column(Float)
    r3_2_subtotal_of_cash_outflow_from_finance = Column(Float)
    r5_1_cash_and_cash_equivalent_at_the_beginning_of_period = Column(Float)
    r5_2_cash_and_cash_equivalent_at_the_end_of_period = Column(Float)


class formBalance(formFinanceTemplate):
    __tablename__ = 'balance_sheet'
    report_date = Column(Date, primary_key=True)
    char_stock_code = Column(String(10), primary_key=True)
    float_assets = Column(Float)
    float_r1_current_assets = Column(Float)
    float_r1_1_bank_and_cash = Column(Float)
    float_r1_2_provision_of_settlement_fund = Column(Float)
    float_r1_3_lent_fund = Column(Float)
    float_r1_4_financial_asset_held_for_trading = Column(Float)
    float_r1_5_derivative_financial_asset = Column(Float)
    float_r1_6_notes_receivable = Column(Float)
    float_r1_7_accounts_receivable = Column(Float)
    float_r1_8_prepayment = Column(Float)
    float_r1_9_insurance_premiums_receivable = Column(Float)
    float_r1_10_cession_premiums_receivable = Column(Float)
    float_r1_11_provision_of_cession_receivable = Column(Float)
    float_r1_12_interest_receivable = Column(Float)
    float_r1_13_dividend_receivable = Column(Float)
    float_r1_14_other_receivable = Column(Float)
    float_r1_15_export_drawback_receivable = Column(Float)
    float_r1_16_allowance_receivable = Column(Float)
    float_r1_17_deposite_recievable = Column(Float)
    float_r1_18_internal_recievables = Column(Float)
    float_r1_19_recoursable_financial_assets_acquired = Column(Float)
    float_r1_20_inventory = Column(Float)
    float_r1_21_deferred_expense = Column(Float)
    float_r1_22_unsettled_gross_and_loss_on_current_asset = Column(Float)
    float_r1_23_long_term_debenture_investment_falling_due_in_a_year = Column(Float)
    float_r1_24_other_current_asset = Column(Float)
    float_r2_non_current_assets = Column(Float)
    float_r2_1_loans_and_payments_on_behalf = Column(Float)
    float_r2_2_financial_asset_available_for_sale = Column(Float)
    float_r2_3_investment_held_to_maturity = Column(Float)
    float_r2_4_long_term_receivable = Column(Float)
    float_r2_5_long_term_equity_investment = Column(Float)
    float_r2_6_other_long_term_investment = Column(Float)
    float_r2_7_investment_real_estate = Column(Float)
    float_r2_8_fixed_asset_original_cost = Column(Float)
    float_r2_9_accmulated_depreciation = Column(Float)
    float_r2_10_fixed_asset_net_value = Column(Float)
    float_r2_11_provision_of_fixed_asset_impairment = Column(Float)
    float_r2_12_fixed_asset = Column(Float)
    float_r2_13_construction_in_progress = Column(Float)
    float_r2_14_construction_supplies = Column(Float)
    float_r2_15_fixed_asset_pending_disposal = Column(Float)
    float_r2_16_bearer_bio_asset = Column(Float)
    float_r2_17_bio_asset = Column(Float)
    float_r2_18_oil_and_gas_asset = Column(Float)
    float_r2_19_intangible_asset = Column(Float)
    float_r2_20_rd_cost = Column(Float)
    float_r2_21_goodwill = Column(Float)
    float_r2_22_long_term_deferred_expense = Column(Float)
    float_r2_23_circulation_right_for_equity_separation = Column(Float)
    float_r2_24_deferred_tax_asset = Column(Float)
    float_r2_25_other_non_current_asset = Column(Float)
    float_liability = Column(Float)
    float_r3_current_liability = Column(Float)
    float_r3_1_short_term_loan = Column(Float)
    float_r3_2_loan_from_central_bank = Column(Float)
    float_r3_3_deposite_from_customer_and_interbank = Column(Float)
    float_r3_4_deposite_fund = Column(Float)
    float_r3_5_financial_liability_held_for_trading = Column(Float)
    float_r3_6_derivative_financial_liability = Column(Float)
    float_r3_7_note_payable = Column(Float)
    float_r3_8_accout_payable = Column(Float)
    float_r3_9_advance_from_customer = Column(Float)
    float_r3_10_fund_from_sale_of_financial_asset_with_repurchasement_agreement = Column(Float)
    float_r3_11_handling_charge_and_commission_payable = Column(Float)
    float_r3_12_employee_benefit_payable = Column(Float)
    float_r3_13_tax_payable = Column(Float)
    float_r3_14_interest_payable = Column(Float)
    float_r3_15_dividend_payable = Column(Float)
    float_r3_16_other_payable = Column(Float)
    float_r3_17_cession_insurance_payable = Column(Float)
    float_r3_18_internal_payable = Column(Float)
    float_r3_19_other_payable = Column(Float)
    float_r3_20_provision_for_expense = Column(Float)
    float_r3_21_accured_liability = Column(Float)
    float_r3_22_account_payable_reinsurance = Column(Float)
    float_r3_23_reserve_for_insurance_contract = Column(Float)
    float_r3_24_acting_trading_security = Column(Float)
    float_r3_25_acting_underwriting_security = Column(Float)
    float_r3_26_international_bill_settlement = Column(Float)
    float_r3_27_domestic_bill_settlement = Column(Float)
    float_r3_28_deferred_income = Column(Float)
    float_r3_29_short_term_bonds_payable = Column(Float)
    float_r3_30_none_current_liability_due_within_one_year = Column(Float)
    float_r3_31_other_none_current_liability = Column(Float)
    float_r4_long_term_liability = Column(Float)
    float_r4_1_long_term_loan = Column(Float)
    float_r4_2_bonds_payable = Column(Float)
    float_r4_3_long_term_payable = Column(Float)
    float_r4_4_specific_payable = Column(Float)
    float_r4_5_estimated_none_current_liability = Column(Float)
    float_r4_6_long_term_deferred_income = Column(Float)
    float_r4_7_deferred_tax_liability = Column(Float)
    float_r4_8_other_none_current_liability = Column(Float)
    float_owner_equity = Column(Float)
    float_r6_equity_attributable_to_parent_company = Column(Float)
    float_r6_1_paid_up_capital = Column(Float)
    float_r6_2_capital_surplus = Column(Float)
    float_r6_3_treasury_stock = Column(Float)
    float_r6_4_specific_reserve = Column(Float)
    float_r6_5_surplus_reserve = Column(Float)
    float_r6_6_general_risk_preperation = Column(Float)
    float_r6_7_unaffirmed_investment_loss = Column(Float)
    float_r6_8_retained_earning = Column(Float)
    float_r6_9_cash_dividend_to_be_distributed = Column(Float)
    float_r6_10_converted_difference_in_foreign_currency_statements = Column(Float)
    float_r7_minority_interest = Column(Float)
    float_liability_and_equity = Column(Float)


balance_column = [
    'float_assets',
    'float_r1_current_assets',
    'float_r1_1_bank_and_cash',
    'float_r1_2_provision_of_settlement_fund',
    'float_r1_3_lent_fund',
    'float_r1_4_financial_asset_held_for_trading',
    'float_r1_5_derivative_financial_asset',
    'float_r1_6_notes_receivable',
    'float_r1_7_accounts_receivable',
    'float_r1_8_prepayment',
    'float_r1_9_insurance_premiums_receivable',
    'float_r1_10_cession_premiums_receivable',
    'float_r1_11_provision_of_cession_receivable',
    'float_r1_12_interest_receivable',
    'float_r1_13_dividend_receivable',
    'float_r1_14_other_receivable',
    'float_r1_15_export_drawback_receivable',
    'float_r1_16_allowance_receivable',
    'float_r1_17_deposite_recievable',
    'float_r1_18_internal_recievables',
    'float_r1_19_recoursable_financial_assets_acquired',
    'float_r1_20_inventory',
    'float_r1_21_deferred_expense',
    'float_r1_22_unsettled_gross_and_loss_on_current_asset',
    'float_r1_23_long_term_debenture_investment_falling_due_in_a_year',
    'float_r1_24_other_current_asset',
    'float_r2_non_current_assets',
    'float_r2_1_loans_and_payments_on_behalf',
    'float_r2_2_financial_asset_available_for_sale',
    'float_r2_3_investment_held_to_maturity',
    'float_r2_4_long_term_receivable',
    'float_r2_5_long_term_equity_investment',
    'float_r2_6_other_long_term_investment',
    'float_r2_7_investment_real_estate',
    'float_r2_8_fixed_asset_original_cost',
    'float_r2_9_accmulated_depreciation',
    'float_r2_10_fixed_asset_net_value',
    'float_r2_11_provision_of_fixed_asset_impairment',
    'float_r2_12_fixed_asset',
    'float_r2_13_construction_in_progress',
    'float_r2_14_construction_supplies',
    'float_r2_15_fixed_asset_pending_disposal',
    'float_r2_16_bearer_bio_asset',
    'float_r2_17_bio_asset',
    'float_r2_18_oil_and_gas_asset',
    'float_r2_19_intangible_asset',
    'float_r2_20_rd_cost',
    'float_r2_21_goodwill',
    'float_r2_22_long_term_deferred_expense',
    'float_r2_23_circulation_right_for_equity_separation',
    'float_r2_24_deferred_tax_asset',
    'float_r2_25_other_non_current_asset',
    'float_liability',
    'float_r3_current_liability',
    'float_r3_1_short_term_loan',
    'float_r3_2_loan_from_central_bank',
    'float_r3_3_deposite_from_customer_and_interbank',
    'float_r3_4_deposite_fund',
    'float_r3_5_financial_liability_held_for_trading',
    'float_r3_6_derivative_financial_liability',
    'float_r3_7_note_payable',
    'float_r3_8_accout_payable',
    'float_r3_9_advance_from_customer',
    'float_r3_10_fund_from_sale_of_financial_asset_with_repurchasement_agreement',
    'float_r3_11_handling_charge_and_commission_payable',
    'float_r3_12_employee_benefit_payable',
    'float_r3_13_tax_payable',
    'float_r3_14_interest_payable',
    'float_r3_15_dividend_payable',
    'float_r3_16_other_payable',
    'float_r3_17_cession_insurance_payable',
    'float_r3_18_internal_payable',
    'float_r3_19_other_payable',
    'float_r3_20_provision_for_expense',
    'float_r3_21_accured_liability',
    'float_r3_22_account_payable_reinsurance',
    'float_r3_23_reserve_for_insurance_contract',
    'float_r3_24_acting_trading_security',
    'float_r3_25_acting_underwriting_security',
    'float_r3_26_international_bill_settlement',
    'float_r3_27_domestic_bill_settlement',
    'float_r3_28_deferred_income',
    'float_r3_29_short_term_bonds_payable',
    'float_r3_30_none_current_liability_due_within_one_year',
    'float_r3_31_other_none_current_liability',
    'float_r4_long_term_liability',
    'float_r4_1_long_term_loan',
    'float_r4_2_bonds_payable',
    'float_r4_3_long_term_payable',
    'float_r4_4_specific_payable',
    'float_r4_5_estimated_none_current_liability',
    'float_r4_6_long_term_deferred_income',
    'float_r4_7_deferred_tax_liability',
    'float_r4_8_other_none_current_liability',
    'float_owner_equity',
    'float_r6_equity_attributable_to_parent_company',
    'float_r6_1_paid_up_capital',
    'float_r6_2_capital_surplus',
    'float_r6_3_treasury_stock',
    'float_r6_4_specific_reserve',
    'float_r6_5_surplus_reserve',
    'float_r6_6_general_risk_preperation',
    'float_r6_7_unaffirmed_investment_loss',
    'float_r6_8_retained_earning',
    'float_r6_9_cash_dividend_to_be_distributed',
    'float_r6_10_converted_difference_in_foreign_currency_statements',
    'float_r7_minority_interest',
    'float_liability_and_equity'
]


class formIncomeStatement(formFinanceTemplate):
    __tablename__ = 'income_statement_sheet'
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


class formCashFlowSupplymentary(formFinanceTemplate):
    __tablename__ = 'cashflow_supplymentary'
    report_period = Column(Date, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    r1_net_profit = Column(Float)
    r2_minority_interest = Column(Float)
    r3_unaffirmed_investment_loss = Column(Float)
    r4_impairment_of_fixed_asset = Column(Float)
    r5_depreciation_of_fixed_asset = Column(Float)
    r6_amortization_of_intangible_asset = Column(Float)
    r7_deferred_asset = Column(Float)
    r8_ = Column(Float)
    r9_ = Column(Float)
    r10_loss_on_disposal_asset = Column(Float)
    r11_loss_on_scrapping_of_fixed_asset = Column(Float)
    r12_ = Column(Float)
    r13_ = Column(Float)
    r14_accrued_liabilities = Column(Float)
    r15_finance_expense = Column(Float)
    r16_invesetment_loss = Column(Float)
    r17_ = Column(Float)
    r18_ = Column(Float)
    r19_decrease_in_inventory = Column(Float)
    r20_decrease_in_operating_receivables = Column(Float)
    r21_increase_in_operating_payables = Column(Float)
    r22_ = Column(Float)
    r23_ = Column(Float)
    r24_other = Column(Float)
    r25_net_cashflow_from_operating_activities = Column(Float)
    r26_ = Column(Float)
    r27_ = Column(Float)
    r28_ = Column(Float)
    r29_cash_at_the_end_of_period = Column(Float)
    r30_cash_at_the_beginning_of_period = Column(Float)
    r31_cash_equivalent_at_the_end_of_period = Column(Float)
    r32_cash_equivalent_at_the_beginning_of_period = Column(Float)
    r33_net_increase_in_cash_and_cash_equivalent = Column(Float)


"""

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
