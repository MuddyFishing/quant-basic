# -*- coding:utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

import pandas as pd
import numpy as np
from collections import OrderedDict


class FiscalData:
    def __init__(self, ticker='600332'):
        self.ticker = ticker
        self.fiscal_data = self.load_fiscal_data(ticker, "20141231", "20170930")
        self.historical_years = self.fiscal_data['endDate'].apply(lambda x: x[:4]).tolist()
        self.future_years = [str(max([int(year) for year in self.historical_years]) + i) for i in range(1, 11)]
        self.basic_assumption_terms = OrderedDict([('grossMargin', u"综合毛利率"), ('revenueGrowth', u"销售收入增长率")
                                                      , ('adminExp2revenue', u"一般行政开支占主营收入比例")
                                                      , ('salesExp2revenue', u"销售费用/销售收入"),
                                                   ('NoperateIncomeExp', u"营业外收支")
                                                      , ('incomeTaxRatio', u"所得税税率")
                                                      , ('surplusReserveRatio', u"盈余公积提取比例"),
                                                   ('mainBusinessTaxRate', u"主营业务税率")
                                                      , ('otherBizProfit', u"其他业务利润"),
                                                   ('researchExp2revenue', u"研发费用占主营收入比例")
                                                      , ('dividendRatio', u"股利分配比率")
                                                      , ('notesReceivable2revenue', u"应收票据/销售收入")
                                                      , ('accountsReceivableTurnoverDays', u"应收帐款周转天数（相对于销售收入）")
                                                      , ('otherReceivable2revenue', u"其他应收款/销售收入")
                                                      , ('prepayment2cogs', u"预付账款/销售成本")
                                                      , ('inventoriesTurnoverDays', u"存货周转天数（相对于销货成本）")
                                                      , ('prepaidExpense2salesAdminExpense', u"待摊费用和其他流动资产/营业费用+管理费用")
                                                      , ('notesPayable2cogs', u"应付票据/销货成本")
                                                      , ('accountsPayableTurnoverDays', u"应付帐款周转天数（相对于销货成本）")
                                                      , ('advanceReceipts2revenue', u"预收账款/销售收入"),
                                                   ('payrollPayable2cogs', u"应付职工薪酬/销货成本")
                                                      , ('taxesPayable2tax', u"应交税费/主营税金+所得税")
                                                      , ('othCL2operCost', u"其他流动负债比经营成本总额")
                                                      , ('badDebts2AR', u"坏帐准备比应收帐款")
                                                      , ('othNCAIncrease', u"其他长期资产绝对增加"),
                                                   ('othNCLIncrease', u"其他长期负债绝对增加")
                                                      , ('minorityGain2EBIT', u"少数股东损益占税前利润比例")
                                                      , ('minorityDividendRatio', u"少数股东权益分红比例")
                                                      , ('cashCEquiv2revenue', u"最低现金余额占主营收入比例")
                                                      , ('surplusCashRate', u"盈余现金利率")
                                                      , ('longDebtRate', u"公司长期债务利率")
                                                      , ('cyclicLoanRate', u"循环贷款利率")
                                                      , ('paidInCapital', u"原始总股本")
                                                      , ('ppeDiscountAcc', u"期末累计折旧")
                                                      , ('accruedExpenses2salesAdminExpense', u"预提费用/营业费用+管理费用")])
        self.invest_assumption_terms = OrderedDict([('tradingFAPred', u"交易性金融资产期末余额"),
                                                    ('availForSaleFaPred', u"可供出售金融资产期末余额"),
                                                    ('htmInvestPred', u"持有至到期投资期末余额"),
                                                    ('LTEquityInvestPredCost', u"长期股权投资（成本法）期末余额"),
                                                    ('LTEquityInvestPredEquity', u"长期股权投资（权益法）期末余额"),
                                                    ('investRealEstatePred', u"投资性房地产期末余额"),
                                                    ('PPEPred', u"固定资产合计"), ('intangiblePred', u"期末无形资产"),
                                                    ('capitalExpansionPred', u"股本扩充"),
                                                    ('commonBondPred', u"普通债期末余额"),
                                                    ('convertibleBondPred', u"可转债期末余额"), ('LTBorrPred', u"期末长期贷款"),
                                                    ('fairValueChangePred', u"公允价值变动合计"),
                                                    ('PPEImpairment', u"固定资产当期计提损失准备"),
                                                    ('LTEquityInvestCostImpairment', u"长期股权投资（成本法）当期计提损失准备"),
                                                    ('LTEquityInvestEquityImpairment', u"长期股权投资（权益法）当期计提损失准备"),
                                                    ('intangibleImpairment', u"无形资产当期计提损失准备"),
                                                    ('htmInvestImpairment', u"持有至到期当期计提损失准备"),
                                                    ('goodwillImpairment', u"商誉当期计提损失准备"),
                                                    ('tradingFAFairValueChange', u"交易性金融资产公允价值变动"),
                                                    ('investRealEstateFairValueChange', u"投资性房地产公允价值变动"),
                                                    ('availForSaleFaFairValueChange', u"可供出售金融资产公允价值变动"),
                                                    ('htmInvestReturn', u"持有至到期当期投资收益"),
                                                    ('LTEquityInvestCostReturn', u"长期股权投资（成本法）当期投资收益"),
                                                    ('LTEquityInvestEquityReturn', u"长期股权投资（权益法）当期投资收益"),
                                                    ('PPEDepreciation', u"固定资产当期计提折旧"),
                                                    ('intangibleAmortization', u"无形资产当期摊销"),
                                                    ('longDebtExpense', u"长期贷款利息费用"),
                                                    ('dividendCurPeriod', u"当期分红")])
        self.basic_assumption_data = pd.DataFrame()
        self.invest_assumption_data = pd.DataFrame()
        return

    def load_fiscal_data(self, stock, start_date="20141231", end_date="20170930"):
        bs = DataAPI.FdmtBSGet(ticker=stock, secID=u"", reportType=u"", endDate=end_date, beginDate=start_date, \
                               publishDateEnd=u"", publishDateBegin=u"", \
                               endDateRep="", beginDateRep="", beginYear="", endYear="", fiscalPeriod="", \
                               field=u"", pandas="1").drop(
            ['endDateRep', 'secID', 'partyID', 'secShortName', 'exchangeCD', 'actPubtime', 'mergedFlag', 'reportType',
             'accoutingStandards', 'currencyCD'], axis=1)
        bs = bs.sort_values(by=['endDate', 'publishDate', 'fiscalPeriod'],
                            ascending=[True, True, False]).drop_duplicates(subset=['endDate'], keep='first')
        income = DataAPI.FdmtISGet(ticker=stock, secID=u"", reportType=u"", endDate=end_date, beginDate=start_date, \
                                   publishDateEnd=u"", publishDateBegin=u"", \
                                   endDateRep="", beginDateRep="", beginYear="", endYear="", fiscalPeriod="", \
                                   field=u"", pandas="1").drop(
            ['endDateRep', 'secID', 'partyID', 'secShortName', 'exchangeCD', 'actPubtime', 'mergedFlag', 'reportType',
             'accoutingStandards', 'currencyCD'], axis=1)
        income = income.sort_values(by=['endDate', 'publishDate', 'fiscalPeriod'],
                                    ascending=[True, True, False]).drop_duplicates(subset=['endDate'], keep='first')
        cf = DataAPI.FdmtCFGet(ticker=stock, secID=u"", reportType=u"", endDate=end_date, beginDate=start_date, \
                               publishDateEnd=u"", publishDateBegin=u"", \
                               endDateRep="", beginDateRep="", beginYear="", endYear="", fiscalPeriod="", \
                               field=u"", pandas="1").drop(
            ['endDateRep', 'secID', 'partyID', 'secShortName', 'exchangeCD', 'actPubtime', 'mergedFlag', 'reportType',
             'accoutingStandards', 'currencyCD'], axis=1)
        cf = cf.sort_values(by=['endDate', 'publishDate', 'fiscalPeriod'],
                            ascending=[True, True, False]).drop_duplicates(subset=['endDate'], keep='first')
        cfs = DataAPI.FdmtCfsGet(ticker=stock, secID=u"", reportType=u"", endDate=u"", beginDate=u"2013-09-30", \
                                 beginYear="", endYear="", fiscalPeriod="", \
                                 field=u"", pandas="1").drop(
            ['endDateRep', 'secID', 'secShortName', 'exchangeCD', 'mergedFlag', 'reportType', 'currencyCD'], axis=1)
        cfs = cfs.sort_values(by=['endDate', 'publishDate', 'fiscalPeriod'],
                              ascending=[True, True, False]).drop_duplicates(subset=['endDate'], keep='first')
        cfs['fiscalPeriod'] = cfs['fiscalPeriod'].astype(int)
        cfs['publishDate'] = cfs['publishDate'].apply(lambda x: x[:10])
        bs = bs.merge(income, left_on=['ticker', 'endDate', 'publishDate', 'fiscalPeriod'],
                      right_on=['ticker', 'endDate', 'publishDate', 'fiscalPeriod'], suffixes=('', '_y'))
        bs = bs.merge(cf, left_on=['ticker', 'endDate', 'publishDate', 'fiscalPeriod'],
                      right_on=['ticker', 'endDate', 'publishDate', 'fiscalPeriod'], suffixes=('', '_y'))
        bs['fiscalPeriod'] = bs['fiscalPeriod'].astype(int)
        bs = bs.merge(cfs, left_on=['ticker', 'endDate', 'publishDate', 'fiscalPeriod'],
                      right_on=['ticker', 'endDate', 'publishDate', 'fiscalPeriod'], how='inner', suffixes=('', '_y'))
        bs = bs.fillna(0.0)
        bs = bs[bs['fiscalPeriod'] == 12]
        bs['endDate'] = bs['endDate'].apply(lambda x: x[:4])
        bs['badDebts'] = bs['assetsImpairLoss']  # 现金流量表附表中应该有披露
        return bs

    def get_fiscal_data(self):
        return self.fiscal_data

    def basic_indicator(self):
        """
        由于DataAPI.FdmtISGet中没有研发费用，所以我们忽略相关指标
        也忽略"其他业务利润","股利分配比率","预提费用比营业费用和管理费用"这两项
        """
        bs = self.fiscal_data
        # 盈利能力
        bs['grossMargin'] = (bs['tRevenue'] - bs['COGS']) / bs['tRevenue']
        bs['revenueGrowth'] = bs['revenue'].pct_change(periods=1)
        bs['adminExp2revenue'] = bs['adminExp'] / bs['revenue']
        bs['salesExp2revenue'] = bs['sellExp'] / bs['revenue']
        bs['NoperateIncomeExp'] = bs['NoperateIncome'] - bs['NoperateExp']
        bs['incomeTaxRatio'] = bs['incomeTax'] / bs['TProfit']
        bs['surplusReserveRatio'] = 0.1
        bs['mainBusinessTaxRate'] = 0.0062
        bs['otherBizProfit'] = 0.0
        bs['researchExp2revenue'] = 0.0
        bs['dividendRatio'] = 0.0
        # 营运效率
        bs['notesReceivable2revenue'] = bs['NotesReceiv'] / bs['revenue']
        bs['accountsReceivableTurnoverDays'] = 365.0 / bs['revenue'] * bs['AR']
        bs['otherReceivable2revenue'] = bs['othReceiv'] / bs['revenue']
        bs['prepayment2cogs'] = bs['prepayment'] / (bs['COGS'] - bs['bizTaxSurchg'])
        bs['inventoriesTurnoverDays'] = 365.0 / (bs['COGS'] - bs['bizTaxSurchg']) * bs['inventories'].rolling(window=2,
                                                                                                              min_periods=1,
                                                                                                              center=False).mean()
        bs['prepaidExpense2salesAdminExpense'] = (bs['TCA'] - bs['cashCEquiv'] - bs['NotesReceiv'] - bs['divReceiv'] -
                                                  bs['AR'] - bs['tradingFA'] - bs['othReceiv'] - bs['prepayment'] - bs[
                                                      'inventories']) / (bs['sellExp'] + bs['adminExp'])
        bs['notesPayable2cogs'] = bs['NotesPayable'] / (bs['COGS'] - bs['bizTaxSurchg'])
        bs['accountsPayableTurnoverDays'] = 365.0 / (bs['COGS'] - bs['bizTaxSurchg']) * bs['AP'].rolling(window=2,
                                                                                                         min_periods=1,
                                                                                                         center=False).mean()
        bs['advanceReceipts2revenue'] = bs['advanceReceipts'] / bs['revenue']
        bs['payrollPayable2cogs'] = bs['payrollPayable'] / (bs['COGS'] - bs['bizTaxSurchg'])
        bs['taxesPayable2tax'] = bs['taxesPayable'] / (bs['bizTaxSurchg'] + bs['incomeTax'])
        bs['othCL2operCost'] = bs['othCL'] / (bs['COGS'] - bs['bizTaxSurchg'] + bs['sellExp'] + bs['adminExp'])
        bs['badDebts2AR'] = 0.045
        bs['othNCAIncrease'] = bs['othNCA']
        bs['othNCLIncrease'] = bs['othNCL']
        bs['minorityGain2EBIT'] = bs['minorityGain'] / bs['TProfit']
        bs['minorityDividendRatio'] = 0.0
        bs['accruedExpenses2salesAdminExpense'] = 0.0
        # 债务和利息
        bs['cashCEquiv2revenue'] = bs['cashCEquiv'] / bs['tRevenue']
        bs['surplusCashRate'] = 0.045
        bs['longDebtRate'] = 0.065
        bs['cyclicLoanRate'] = 0.045
        # 总股本
        bs['paidInCapital'] = bs['paidInCapital']
        bs['ppeDiscountAcc'] = bs['FAOGPBDepr'].cumsum()
        self.fiscal_data = bs
        return bs

    def basic_assumption(self):
        """
        最终要的变量是营收增速、毛利率、一般行政开销占主营比例、销售费用/销售收入、营业外支出，一般大家预估未来3年的各年情况，其余年份取第三年相同值；
        有些指标需要余公司确认，比如少数股东权益分红比例、最低现金金额占主营收入比例等
        """
        bs = self.fiscal_data
        data = []
        data.append(bs[['endDate'] + self.basic_assumption_terms.keys()].iloc[-1].tolist())
        for idx, year in enumerate(self.future_years):
            tmp = [year]
            for col in self.basic_assumption_terms:
                if col in ['othNCAIncrease', 'othNCAIncrease']:
                    tmp.append(0.0)
                else:
                    tmp.append(bs[col].iloc[-1])
            data.append(tmp)
        basic_assumption_data = pd.DataFrame(data=data, columns=['endDate'] + self.basic_assumption_terms.keys())
        basic_assumption_data['revenueGrowth'].iloc[-10:] = np.array(
            [-0.0535, 0.2738, 0.2080, 0.2080, 0.2080, 0.2080, 0.2080, 0.2080, 0.2080, 0.2080])
        basic_assumption_data['grossMargin'].iloc[-10:] = np.array(
            [0.2916, 0.2910, 0.2860, 0.2860, 0.2860, 0.2860, 0.2860, 0.2860, 0.2860, 0.2860])
        basic_assumption_data['adminExp2revenue'].iloc[-10:] = np.array(
            [0.079, 0.068, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065])
        basic_assumption_data['salesExp2revenue'].iloc[-10:] = np.array(
            [0.074, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07])
        basic_assumption_data['NoperateIncomeExp'].iloc[-10:] = np.array(
            [80000000, 80000000, 80000000, 80000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        basic_assumption_data['incomeTaxRatio'].iloc[-10:] = np.array(
            [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12])
        basic_assumption_data['inventoriesTurnoverDays'].iloc[-10:] = np.array(
            [70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0])
        basic_assumption_data['minorityGain2EBIT'].iloc[-10:] = np.array(
            [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        self.basic_assumption_data = basic_assumption_data
        return self.basic_assumption_data.rename(columns=self.basic_assumption_terms)

    def invest_assumption(self):
        def predict_assets_method1(bs, col, cur_period_cost_increase, cur_fair_value_change):
            """
            适用于交易性金融资产、可供出售金融资产、投资性房地产
            """
            period_end_cost = bs[col].iloc[-1]
            period_end_fair_value_change = 0.0
            data = []
            for idx, year in enumerate(self.future_years):
                init = period_end_cost
                period_end_cost = cur_period_cost_increase[idx] + init
                period_end_fair_value_change += cur_fair_value_change[idx]
                data.append([year, init + cur_period_cost_increase[idx] + period_end_fair_value_change,
                             cur_period_cost_increase[idx]])
            invest_assumption_data = pd.DataFrame(data=data, columns=['endDate', col + 'Pred', col + 'FairValueChange'])
            return invest_assumption_data

        def predict_assets_method2(bs, col, cur_period_cost_increase, cur_period_impairment_prepare, coupon_rate):
            """
            适用于持有至到期资产
            """
            period_end_balance = bs[col].iloc[-1]
            period_end_impairment = 0.0
            data = []
            for idx, year in enumerate(self.future_years):
                init = period_end_balance
                invest_return = (init + period_end_impairment) * coupon_rate[idx] + cur_period_cost_increase[idx] * \
                                                                                    coupon_rate[idx] / 2.0
                period_end_impairment += cur_period_impairment_prepare[idx]
                period_end_balance = init + cur_period_cost_increase[idx] - cur_period_impairment_prepare[idx]
                data.append([year, period_end_balance, cur_period_impairment_prepare[idx], invest_return,
                             cur_period_cost_increase[idx]])
            invest_assumption_data = pd.DataFrame(data=data, columns=['endDate', col + 'Pred', 'htmInvestImpairment',
                                                                      'htmInvestReturn', 'htmInvestFairValueChange'])
            return invest_assumption_data

        def predict_assets_method3(col, cur_period_cost_increase, cur_period_impairment_prepare, invest_return):
            """
            适用于长期股权投资(成本法)
            """
            period_end_balance = 0.0
            period_end_impairment = 0.0
            data = []
            for idx, year in enumerate(self.future_years):
                init = period_end_balance
                period_end_impairment += cur_period_impairment_prepare[idx]
                period_end_balance = init + cur_period_cost_increase[idx] - cur_period_impairment_prepare[idx]
                data.append([year, period_end_balance, cur_period_impairment_prepare[idx], invest_return[idx],
                             cur_period_cost_increase[idx]])
            invest_assumption_data = pd.DataFrame(data=data, columns=['endDate', col + 'Pred' + 'Cost',
                                                                      'LTEquityInvestCostImpairment',
                                                                      'LTEquityInvestCostReturn',
                                                                      'LTEquityInvestCostFairValueChange'])
            return invest_assumption_data

        def predict_assets_method4(bs, col, cur_period_cost_increase, cur_period_impairment_prepare, invest_return,
                                   dividend_ratio):
            """
            适用于长期股权投资(权益法)
            """
            period_end_balance = bs[col].iloc[-1]
            period_end_impairment = 0.0
            invest_return_acc = 0.0
            data = []
            for idx, year in enumerate(self.future_years):
                init = period_end_balance
                period_cur_dividend = invest_return_acc * dividend_ratio[idx]
                invest_return_acc += invest_return[idx] - period_cur_dividend
                period_end_impairment += cur_period_impairment_prepare[idx]
                period_end_balance = init + cur_period_cost_increase[idx] + invest_return[idx] - period_cur_dividend - \
                                     cur_period_impairment_prepare[idx]
                data.append([year, period_end_balance, cur_period_impairment_prepare[idx], invest_return[idx],
                             period_cur_dividend, cur_period_cost_increase[idx]])
            invest_assumption_data = pd.DataFrame(data=data, columns=['endDate', col + 'Pred' + 'Equity',
                                                                      'LTEquityInvestEquityImpairment',
                                                                      'LTEquityInvestEquityReturn', 'dividendCurPeriod',
                                                                      'LTEquityInvestEquityFairValueChange'])
            return invest_assumption_data

        def predict_assets_method5(bs, basic_assumption, ppe_growth, ppe_scale_spread_demand, cip_conversion,
                                   cur_period_impairment_prepare, discount_ratio):
            """
            固定资产投资计划
            """
            period_end_cip_ori = bs['CIP'].iloc[-1] + bs['constMaterials'].iloc[-1]
            period_end_ppe_ori = bs['fixedAssets'].iloc[-1]
            period_cur_discount = bs['FAOGPBDepr'].iloc[-1]
            discount = period_cur_discount / period_end_ppe_ori
            period_end_discount_acc = bs['ppeDiscountAcc'].iloc[-1]
            period_end_ppe_netvalue = bs['CIP'].iloc[-1]
            impairment_prepare_acc = bs['assetsImpairLoss'].iloc[-1]
            ppe_acc = period_end_cip_ori + period_end_ppe_netvalue - impairment_prepare_acc
            sales_revenue = bs['revenue'].iloc[-1]
            data = []
            for idx, year in enumerate(self.future_years):
                sales_revenue *= 1 + basic_assumption['revenueGrowth'].iloc[idx + 1]
                internal_demand = sales_revenue * ppe_growth[idx]
                ppe_invest_total = internal_demand + ppe_scale_spread_demand[idx]
                period_start_cip_ori = ppe_invest_total + period_end_cip_ori
                cip2ppe = cip_conversion[idx] * period_start_cip_ori
                period_end_cip_ori = period_start_cip_ori * (1 - cip_conversion[idx])
                period_cur_discount = period_end_ppe_ori * discount_ratio[idx] + cip2ppe * discount_ratio[idx] / 2.0
                period_end_ppe_ori += cip2ppe
                period_end_discount_acc += period_cur_discount
                period_end_ppe_netvalue = period_end_ppe_ori - period_end_discount_acc
                impairment_prepare_acc += cur_period_impairment_prepare[idx]
                ppe_acc = period_end_cip_ori + period_end_ppe_netvalue - impairment_prepare_acc
                data.append([year, ppe_acc, cur_period_impairment_prepare[idx], period_cur_discount, ppe_invest_total])
            invest_assumption_data = pd.DataFrame(data=data,
                                                  columns=['endDate', 'PPEPred', 'PPEImpairment', 'PPEDepreciation',
                                                           'PPETotalInvest'])
            return invest_assumption_data

        def predict_assets_method6(bs, cur_period_increase_intangible, cur_period_amortization_ratio,
                                   cur_period_impairment_prepare):
            """
            无形资产投资
            """
            period_start_intangible = bs['intanAssets'].iloc[-2] if len(bs.index) > 1 else 0.0
            period_cur_amortization = bs['intanAssetsAmor'].iloc[-1]
            period_end_intangible = bs['intanAssets'].iloc[-1]
            period_cur_intangible_increase = period_end_intangible - period_start_intangible + period_cur_amortization
            period_amortization_ratio = period_cur_amortization / (
            period_start_intangible + period_cur_intangible_increase / 2.0)
            impairment_prepare_acc = 0.0
            data = []
            for idx, year in enumerate(self.future_years):
                init = cur_period_increase_intangible[idx] + period_end_intangible
                period_cur_amortization = period_end_intangible * cur_period_amortization_ratio[
                    idx] + period_cur_intangible_increase * cur_period_amortization_ratio[idx] / 2.0
                impairment_prepare_acc += cur_period_impairment_prepare[idx]
                period_end_intangible = init - period_cur_amortization - cur_period_impairment_prepare[idx]
                data.append([year, period_end_intangible, cur_period_impairment_prepare[idx], period_cur_amortization,
                             cur_period_increase_intangible[idx]])
            invest_assumption_data = pd.DataFrame(data=data,
                                                  columns=['endDate', 'intangiblePred', 'intangibleImpairment',
                                                           'intangibleAmortization', 'intangibleFairValueChange'])
            return invest_assumption_data

        def predict_assets_method7(bs, basic_assumption, col, cur_period_cost_increase):
            period_end_cost = bs[col].iloc[-1]
            data = []
            for idx, year in enumerate(self.future_years):
                init = period_end_cost
                period_end_cost = cur_period_cost_increase[idx] + init
                longDebtExpense = (init + period_end_cost) / 2.0 * basic_assumption['longDebtRate'].iloc[idx + 1]
                data.append([year, period_end_cost, longDebtExpense])
            invest_assumption_data = pd.DataFrame(data=data, columns=['endDate', 'LTBorrPred', 'longDebtExpense'])
            return invest_assumption_data

        bs = self.fiscal_data
        basic_assumption = self.basic_assumption_data
        num = len(self.future_years)
        # 交易性金融资产
        tradingFAPred = predict_assets_method1(bs, 'tradingFA', np.zeros(num), np.zeros(num))
        # 可供出售金融资产
        availForSaleFaPred = predict_assets_method1(bs, 'availForSaleFa', np.zeros(num), np.zeros(num))
        # 持有至到期投资
        htmInvestPred = predict_assets_method2(bs, 'htmInvest', np.zeros(num), np.zeros(num), np.ones(num) * 0.1)
        # 长期股权投资（成本法）
        LTEquityInvestPredCost = predict_assets_method3('LTEquityInvest', np.zeros(num), np.zeros(num),
                                                        np.ones(num) * 40000.0)
        # 长期股权投资（权益法）
        LTEquityInvestPredEquity = predict_assets_method4(bs, 'LTEquityInvest', np.zeros(num), np.zeros(num),
                                                          np.ones(num) * 40000.0, np.ones(num) * 0.05)
        # 投资性房地产
        investRealEstatePred = predict_assets_method1(bs, 'investRealEstate', np.zeros(num), np.zeros(num))
        # 固定资产投资计划
        ppePred = predict_assets_method5(bs, basic_assumption, np.ones(num) * 0.03, np.ones(num) * 360000.0,
                                         np.ones(num) * 0.8, np.zeros(num), np.ones(num) * 0.045)
        # 无形资产投资
        intangiblePred = predict_assets_method6(bs, np.zeros(num), np.ones(num) * 0.05, np.zeros(num))
        # 股权融资（配股、转增、回购）
        capitalExpansionPred = pd.DataFrame(data=[[year, i] for year, i in zip(self.future_years, np.zeros(num))],
                                            columns=['endDate', 'capitalExpansionPred'])
        # 普通债
        commonBondPred = pd.DataFrame(data=[[year, i] for year, i in zip(self.future_years, np.zeros(num))],
                                      columns=['endDate', 'commonBondPred'])
        # 可转债
        convertibleBondPred = pd.DataFrame(data=[[year, i] for year, i in zip(self.future_years, np.zeros(num))],
                                           columns=['endDate', 'convertibleBondPred'])
        # 长期银行贷款
        LTBorrPred = predict_assets_method7(bs, basic_assumption, 'LTBorr', np.zeros(num))
        # 公允价值变动收益合计
        fairValueChangePred = pd.DataFrame(data=[[year, i] for year, i in zip(self.future_years, np.zeros(num))],
                                           columns=['endDate', 'fairValueChangePred'])
        # 商誉计提损失准备
        goodwillImpairment = pd.DataFrame(data=[[year, i] for year, i in zip(self.future_years, np.zeros(num))],
                                          columns=['endDate', 'goodwillImpairment'])
        invest_assumption_data = reduce(lambda left, right: pd.merge(left, right, on='endDate'),
                                        [tradingFAPred, availForSaleFaPred, htmInvestPred, LTEquityInvestPredCost,
                                         LTEquityInvestPredEquity, investRealEstatePred, ppePred, intangiblePred,
                                         capitalExpansionPred, commonBondPred, convertibleBondPred, LTBorrPred,
                                         fairValueChangePred, goodwillImpairment])
        self.invest_assumption_data = invest_assumption_data
        return invest_assumption_data.rename(columns=self.invest_assumption_terms)