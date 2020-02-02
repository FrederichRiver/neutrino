#!/usr/bin/python3
import numpy as np
import pandas as pd
from venus.stock_base import StockEventBase, dataLine
from jupiter.utils import read_url, CONF_FILE, trans


class EventFinanceReport(StockEventBase):
    def update_balance_sheet(self, stock_code):
        # get url
        url = read_url("URL_balance", CONF_FILE)
        url = url.format(stock_code[2:])
        # get data
        df = self.fetch_balance_sheet(stock_code)
        print(df)
        if not df.empty:
            dataline = dataLine('balance_sheet')
            try:
                insert_sql_list = dataline.insert_sql(df)
            except Exception as e:
                print(e)
            try:
                #update_sql_list = dataline.update_sql(df, ['stock_code', 'report_period'])
                update_sql_list = dataline.update_sql(df, ['c0', 'c1'])
            except Exception as e:
                print(e)
        for sql in insert_sql_list:
            print(sql)
        print(update_sql_list)
        for sql in update_sql_list:
            print(sql)

    def update_balance_sheet_asset(self, stock_code):
        url = read_url("URL_balance", CONF_FILE)
        url = url.format(stock_code[2:])
        df = self.fetch_balance_sheet(stock_code)
        update_period = '0'
        if not df.empty:
            for index, row in df.iterrows():
                update_sql = (
                    f"UPDATE balance_sheet_template set "
                    f"r1_assets={trans(row[51])},r2_current_assets={trans(row[24])},"
                    f"r3_non_current_assets={trans(row[50])},r4_current_liability={trans(row[83])},"
                    f"r5_long_term_liability={trans(row[92])},r6_total_equity={trans(row[106])},"
                    f"r1_1_bank_and_cash={trans(row[0])}, r1_3_inventory={trans(row[19])},"
                    f"r3_1_fixed_assets={trans(row[36])},r3_2_goodwill={trans(row[45])},"
                    f"r5_1_short_term_loans={trans(row[52])},r5_2_notes_payable={trans(row[58])},"
                    f"r5_3_accounts_payable={trans(row[59])},r6_1_long_term_loans={trans(row[84])},"
                    f"r6_2_bonds_payable={trans(row[85])} "
                    f"WHERE (report_period='{index}' and stock_code='{stock_code}')"
                )
                if index > update_period:
                    update_period = index
                    # print(update_period)
                try:
                    self.mysql.engine.execute(update_sql)
                except Exception as e:
                    print(e)

    def fetch_balance_sheet(self, stock_code):
        """
        read csv data and return a dataframe object.
        """
        # config file is a url file.
        # _, url = read_json('URL_163_MONEY', CONF_FILE)
        url = read_url("URL_balance", CONF_FILE)
        url = url.format(stock_code[2:])
        df = pd.read_csv(url, encoding='gb18030')
        if not df.empty:
            df = df.T
            result = df.iloc[1:]
        else:
            result = df
        result.replace(['--'], np.nan, inplace=True)
        result.columns = ['c'+str(i) for i in range(108)]
        return result

    def update_income_statement(self, stock_code):
        df = self.fetch_income_statement(stock_code)
        update_period = '0'
        if not df.empty:
            for index, row in df.iterrows():
                query_sql = (
                    f"SELECT * from income_statement_template where ("
                    f"report_period='{index}' and stock_code='{stock_code}')")
                # print(query_sql)
                result = self.mysql.engine.execute(query_sql).fetchall()
                # print(result)
                insert_sql = (
                    f"INSERT into income_statement_template (report_period, stock_code,"
                    "r1_total_revenue,r2_total_cost,r3_profit_from_operation,"
                    "r4_net_profit,r1_1_revenue,r1_2_interest_income,"
                    "r1_3_other_operating_income,r2_1_operating_cost,"
                    "r2_2_rd_expense,r2_3_ga_expense,r2_4_selling_expense,"
                    "r2_5_finance_expense),r3_1_non_operating_income,"
                    "r3_2_non_operating_expense,r3_2_disposal_loss_on_non_current_asset,"
                    "r3_4_profit_before_tax,r3_5_income_tax,"
                    "r3_6_unrealized_investment_loss) "
                    f"VALUES ('{index}', '{stock_code}',{trans(row[0])},"
                    f"{trans(row[7])},{trans(row[32])},{trans(row[39])},"
                    f"{trans(row[1])},{trans(row[2])},{trans(row[6])},"
                    f"{trans(row[8])},{trans(row[12])},{trans(row[21])},"
                    f"{trans(row[20])},{trans(row[22])},{trans(row[33])},"
                    f"{trans(row[34])},{trans(row[35])},{trans(row[36])},"
                    f"{trans(row[37])},{trans(row[38])})")
                update_sql = (
                    f"UPDATE income_statement_template set "
                    f"r1_total_revenue={trans(row[0])},"
                    f"r2_total_cost={trans(row[7])},"
                    f"r3_profit_from_operation={trans(row[32])},"
                    f"r4_net_profit={trans(row[39])},"
                    f"r1_1_revenue={trans(row[1])},"
                    f"r1_2_interest_income={trans(row[2])},"
                    f"r1_3_other_operating_income={trans(row[6])},"
                    f"r2_1_operating_cost={trans(row[8])},"
                    f"r2_2_rd_expense={trans(row[12])},"
                    f"r2_3_ga_expense={trans(row[21])},"
                    f"r2_4_selling_expense={trans(row[20])},"
                    f"r2_5_finance_expense={trans(row[22])},"
                    f"r3_1_non_operating_income={trans(row[33])},"
                    f"r3_2_non_operating_expense={trans(row[34])},"
                    f"r3_2_disposal_loss_on_non_current_asset={trans(row[35])},"
                    f"r3_4_profit_before_tax={trans(row[36])},"
                    f"r3_5_income_tax={trans(row[37])},"
                    f"r3_6_unrealized_investment_loss={trans(row[38])} "
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
                f"UPDATE stock_manager set gmt_income='{update_period}' "
                f"WHERE stock_code='{stock_code}'")
            self.mysql.engine.execute(update_date_sql)

    def fetch_income_statement(self, stock_code):
        """
        read csv data and return a dataframe object.
        """
        # config file is a url file.
        # _, url = read_json('URL_163_MONEY', CONF_FILE)
        url = f"http://quotes.money.163.com/service/lrb_{stock_code[2:]}.html"
        df = pd.read_csv(url, encoding='gb18030')
        if not df.empty:
            df = df.T
            result = df.iloc[1:]
        else:
            result = df
        df.replace(['--'], np.nan, inplace=True)
        return result

    def update_cashflow_sheet(self, stock_code):
        url = f"http://quotes.money.163.com/service/xjllb_{stock_code[2:]}.html"
        df = self.fetch_cashflow_sheet(stock_code)
        update_period = '0'
        if not df.empty:
            for index, row in df.iterrows():
                query_sql = (
                    f"SELECT * from cash_flow_sheet where ("
                    f"report_period='{index}' and stock_code='{stock_code}')")
                # print(query_sql)
                result = self.mysql.engine.execute(query_sql).fetchall()
                # print(result)
                insert_sql = (
                    "INSERT into cash_flow_sheet (report_period, stock_code, "
                    "r1_cash_flow_from_operating_activities, "
                    "r2_cash_flow_from_investment, "
                    "r3_cash_flow_from_finance_activities, "
                    "r4_effect_of_foriegn_exchange_rate_changes_on_cash_effect, "
                    "r5_net_increase_in_cash_and_cash_equivalent, "
                    "r1_2_subtotal_of_cash_inflow_from_operating, "
                    "r1_3_subtotal_of_cash_outflow_from_operating, "
                    "r2_1_subtotal_of_cash_inflow_from_investment, "
                    "r2_2_subtotal_of_cash_outflow_from_investment, "
                    "r3_1_subtotal_of_cash_inflow_from_finance, "
                    "r3_2_subtotal_of_cash_outflow_from_finance, "
                    "r5_1_cash_and_cash_equivalent_at_the_beginning_of_period, "
                    "r5_2_cash_and_cash_equivalent_at_the_end_of_period) "
                    f"VALUES ('{index}', '{stock_code}',{trans(row[24])},"
                    f"{trans(row[39])},{trans(row[51])},{trans(row[52])},"
                    f"{trans(row[53])},{trans(row[13])},{trans(row[23])},"
                    f"{trans(row[31])},{trans(row[38])},{trans(row[45])},"
                    f"{trans(row[50])},{trans(row[54])},{trans(row[55])})")
                update_sql = (
                    f"UPDATE cash_flow_sheet set "
                    f"r1_cash_flow_from_operating_activities={trans(row[24])},"
                    f"r2_cash_flow_from_investment={trans(row[39])},"
                    f"r3_cash_flow_from_finance_activities={trans(row[51])},"
                    f"r4_effect_of_foriegn_exchange_rate_changes_on_cash_effect={trans(row[52])},"
                    f"r5_net_increase_in_cash_and_cash_equivalent={trans(row[53])},"
                    f"r1_2_subtotal_of_cash_inflow_from_operating={trans(row[13])},"
                    f"r1_3_subtotal_of_cash_outflow_from_operating={trans(row[23])},"
                    f"r2_1_subtotal_of_cash_inflow_from_investment={trans(row[31])},"
                    f"r2_2_subtotal_of_cash_outflow_from_investment={trans(row[38])},"
                    f"r3_1_subtotal_of_cash_inflow_from_finance={trans(row[45])},"
                    f"r3_2_subtotal_of_cash_outflow_from_finance={trans(row[50])},"
                    f"r5_1_cash_and_cash_equivalent_at_the_beginning_of_period={trans(row[54])},"
                    f"r5_2_cash_and_cash_equivalent_at_the_end_of_period={trans(row[55])} "
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
                f"UPDATE stock_manager set gmt_cashflow='{update_period}' "
                f"WHERE stock_code='{stock_code}'")
            self.mysql.engine.execute(update_date_sql)

    def fetch_cashflow_sheet(self, stock_code):
        """
        read csv data and return a dataframe object.
        """
        # config file is a url file.
        # _, url = read_json('URL_163_MONEY', CONF_FILE)
        url = f"http://quotes.money.163.com/service/xjllb_{stock_code[2:]}.html"
        df = pd.read_csv(url, encoding='gb18030')
        if not df.empty:
            df = df.T
            result = df.iloc[1:]
        else:
            result = df
        df.replace(['--'], np.nan, inplace=True)
        return result

    def update_cashflow_supplymentary(self, stock_code):
        df = self.fetch_cashflow_sheet(stock_code)
        update_period = '0'
        if not df.empty:
            for index, row in df.iterrows():
                query_sql = (
                    f"SELECT * from cash_flow_supplymentary where ("
                    f"report_period='{index}' and stock_code='{stock_code}')")
                # print(query_sql)
                result = self.mysql.engine.execute(query_sql).fetchall()
                # print(result)
                insert_sql = (
                    "INSERT into cash_flow_supplymentary (report_period,"
                    "stock_code,r1_net_profit,r2_minority_interest,"
                    "r3_unaffirmed_investment_loss,"
                    "r4_impairment_of_fixed_asset,"
                    "r5_depreciation_of_fixed_asset,"
                    "r6_amortization_of_intangible_asset,r7_deferred_asset,"
                    "r8_,r9_,r10_loss_on_disposal_asset,"
                    "r11_loss_on_scrapping_of_fixed_asset,r12_,r13_,"
                    "r14_accrued_liabilities,r15_finance_expense,"
                    "r16_invesetment_loss,r17_,r18_,"
                    "r19_decrease_in_inventory,"
                    "r20_decrease_in_operating_receivables,"
                    "r21_increase_in_operating_payables,r22_,r23_,r24_other,"
                    "r25_net_cashflow_from_operating_activities,"
                    "r26_,r27_,r28_,r29_cash_at_the_end_of_period,"
                    "r30_cash_at_the_beginning_of_period,"
                    "r31_cash_equivalent_at_the_end_of_period,"
                    "r32_cash_equivalent_at_the_beginning_of_period,"
                    "r33_net_increase_in_cash_and_cash_equivalent) "
                    f"VALUES ('{index}', '{stock_code}',{trans(row[56])},"
                    f"{trans(row[57])},{trans(row[58])},{trans(row[59])},"
                    f"{trans(row[60])},{trans(row[61])},{trans(row[62])},"
                    f"{trans(row[63])},{trans(row[64])},{trans(row[65])},"
                    f"{trans(row[66])},{trans(row[67])},{trans(row[68])},"
                    f"{trans(row[69])},{trans(row[70])},{trans(row[71])},"
                    f"{trans(row[72])},{trans(row[73])},{trans(row[74])},"
                    f"{trans(row[75])},{trans(row[76])},{trans(row[77])},"
                    f"{trans(row[78])},{trans(row[79])},{trans(row[80])},"
                    f"{trans(row[81])},{trans(row[82])},{trans(row[83])},"
                    f"{trans(row[84])},{trans(row[85])},{trans(row[86])},"
                    f"{trans(row[87])},{trans(row[88])})"
                    )
                update_sql = (
                    f"UPDATE cash_flow_sheet set "
                    f"r1_net_profit = {trans(row[56])},"
                    f"r2_minority_interest = {trans(row[57])},"
                    f"r3_unaffirmed_investment_loss = {trans(row[58])},"
                    f"r4_impairment_of_fixed_asset = {trans(row[59])},"
                    f"r5_depreciation_of_fixed_asset = {trans(row[60])},"
                    f"r6_amortization_of_intangible_asset = {trans(row[61])},"
                    f"r7_deferred_asset = {trans(row[62])},"
                    f"r8_ = {trans(row[63])},"
                    f"r9_ = {trans(row[64])},"
                    f"r10_loss_on_disposal_asset = {trans(row[65])},"
                    f"r11_loss_on_scrapping_of_fixed_asset = {trans(row[66])},"
                    f"r12_ = {trans(row[67])},"
                    f"r13_ = {trans(row[68])},"
                    f"r14_accrued_liabilities = {trans(row[69])},"
                    f"r15_finance_expense = {trans(row[70])},"
                    f"r16_invesetment_loss = {trans(row[71])},"
                    f"r17_ = {trans(row[72])},"
                    f"r18_ = {trans(row[73])},"
                    f"r19_decrease_in_inventory = {trans(row[74])},"
                    f"r20_decrease_in_operating_receivables = {trans(row[75])},"
                    f"r21_increase_in_operating_payables = {trans(row[76])},"
                    f"r22_ = {trans(row[77])},"
                    f"r23_ = {trans(row[78])},"
                    f"r24_other = {trans(row[79])},"
                    f"r25_net_cashflow_from_operating_activities = {trans(row[80])},"
                    f"r26_ = {trans(row[81])},"
                    f"r27_ = {trans(row[82])},"
                    f"r28_ = {trans(row[83])},"
                    f"r29_cash_at_the_end_of_period = {trans(row[84])},"
                    f"r30_cash_at_the_beginning_of_period = {trans(row[85])},"
                    f"r31_cash_equivalent_at_the_end_of_period = {trans(row[86])},"
                    f"r32_cash_equivalent_at_the_beginning_of_period = {trans(row[87])},"
                    f"r33_net_increase_in_cash_and_cash_equivalent = {trans(row[88])} "
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
                f"UPDATE stock_manager set gmt_cashflow='{update_period}' "
                f"WHERE stock_code='{stock_code}'")
            self.mysql.engine.execute(update_date_sql)
