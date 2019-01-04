
-- ----------------------------
-- Table structure for stock
-- ----------------------------
DROP TABLE IF EXISTS `xjllb`;
CREATE TABLE `xjllb` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `report_date` date NOT NULL,
  `sh_code` varchar(15) NOT NULL,
  #`sh_name` varchar(300) NOT NULL,
  `sale_or_work_income` decimal(20,2),#销售商品、提供劳务收到的现金(万元)
  `net_sale_profit` decimal(20,2) ,#经营活动产生的现金流量净额(万元)
  `selling_income_cash` decimal(20,2) ,#处置固定资产、无形资产和其他长期资产所收回的现金净额(万元)
  `selling_corop_income` decimal(20,2) ,#处置子公司及其他营业单位收到的现金净额(万元)
  `shoping_out_cash` decimal(20,2),#购建固定资产、无形资产和其他长期资产所支付的现金(万元)
  `investment_total` decimal(20,2) , #投资活动产生的现金流量净额(万元)
  `financing_in` decimal(20,2) ,#取得借款收到的现金(万元)
  `financing_out` decimal(20,2) ,#偿还债务支付的现金(万元)
  `financing_total` decimal(20,2) ,#筹资活动产生的现金流量净额(万元)
  `cash_add` decimal(20,2), #现金及现金等价物净增加额(万元)
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


DROP TABLE
IF EXISTS `zcfzb`;

CREATE TABLE `zcfzb` (
  `id` BIGINT (20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `report_date` date NOT NULL,
  `sh_code` VARCHAR (15) NOT NULL,

  `monetary_resources` DECIMAL (20, 2) ,
  #货币资金(万元)
  `notes_receivable` DECIMAL (20, 2),
  #应收票据
  `accounts_receivable` DECIMAL (20, 2),
  #应收账款
  `prepayments` DECIMAL (20, 2),
  #预付款项(万元)
  `others_accounts_receivable` DECIMAL (20, 2),
  #其他应收账款
  `inventory` DECIMAL (20, 2),
  #存货(万元)
  `other_flow_assert` DECIMAL (20, 2),
  #其他流动资产合计(万元)
  `flow_assert` DECIMAL (20, 2),
  #流动资产合计(万元)
  `fixed_assets` DECIMAL (20, 2),
  #固定资产
  `uncompleted_construction` DECIMAL (20, 2),

  #在建工程
  `investment_real_estate` DECIMAL (20, 2),
  #投资性房地产

  `long_pre_ability` DECIMAL (20, 2),
  #长期待摊费用(万元)

  `other_non_flow_assert` DECIMAL (20, 2),
  #其他非流动资产合计(万元)
  `non_flow_assert` DECIMAL (20, 2),
  #非流动资产合计(万元)
  `assert_total` DECIMAL (20, 2),
  #资产总计(万元)
  `short_term_liability` DECIMAL(20, 2),
  #短期负债
  `should_pay_notes` DECIMAL(20, 2),
  #应付票据
  `should_pay_account` DECIMAL(20, 2),
  #应付账款

  `other_should_pay_account` DECIMAL(20, 2),
  #其他应付账款

  `other_flow_liabilities` DECIMAL (20, 2) ,
  #其他流动负债
  `flow_liabilities` DECIMAL (20, 2) ,
  #流动负债合计(万元)

   `long_term_liability` DECIMAL(20, 2),
  #长期负债

  `other_non_flow_liabilities` DECIMAL (20, 2) ,
  #其他非流动负债合计(万元)
  `non_flow_liabilities` DECIMAL (20, 2) ,
  #非流动负债合计(万元)
  `liabilities_total` DECIMAL (20, 2) ,
  #负债合计(万元)
  `undistributed_profit` DECIMAL (20, 2) ,
  #未分配利润(万元)
  `owners_equity` DECIMAL (20, 2) ,
  #所有者权益(或股东权益)合计(万元)
  `liabilities_and_equity` DECIMAL (20, 2) ,
  #负债和所有者权益(或股东权益)总计(万元)
  PRIMARY KEY (`id`)
) ENGINE = INNODB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;



DROP TABLE IF EXISTS `lrb`;
CREATE TABLE `lrb` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `report_date` date NOT NULL,
  `sh_code` varchar(15) NOT NULL,
  #`sh_name` varchar(300) NOT NULL,

`total_sales_revenue` decimal(20,2) , #营业总收入(万元)
`sales_revenue` decimal(20,2) , #营业收入(万元)
`total_operation_cost` decimal(20,2),#营业总成本
`operation_cost` decimal(20,2), #营业成本
`sales_profit` decimal(20,2),#营业利润
`nonbusiness_income` decimal(20,2),#营业外收入
`nonbusiness_cost` decimal(20,2),#营业外支出
`net_profit` decimal(20,2) , #净利润(万元)
`earning_per_sharing` decimal(20,2)  , #基本每股收益
`ex_earning_per_sharing` decimal(20,2)  , #稀释每股收益
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;




select
zcfzb.report_date,
(monetary_resources-short_term_liability-long_term_liability)/monetary_resources as "货币资金-借债/货币资金",
accounts_receivable/assert_total as "应收账款/总资产",
others_accounts_receivable/lrb.total_sales_revenue as "其他应收款/收入",
other_should_pay_account/liabilities_total as "其他应付款/负债总额",
prepayments/lrb.operation_cost as "预付款/营业成本",
inventory/lrb.sales_revenue as "存货/毛利率",
long_pre_ability as "长期待摊费用",
investment_real_estate/lrb.net_profit as "投资性房产/净利润幅度",
owners_equity/liabilities_and_equity as "所有者权益/总资产",
(flow_assert+fixed_assets)/assert_total as "生产资产/总资产",
(monetary_resources-short_term_liability)/monetary_resources as "货币资金-短期负债/货币资金"

 from zcfzb INNER JOIN lrb on zcfzb.report_date=lrb.report_date and zcfzb.sh_code=lrb.sh_code  WHERE zcfzb.sh_code='600009';



select
lrb.report_date,
xjllb.net_sale_profit/net_profit as "经营现金流净额/净利润",
(sales_revenue-operation_cost)/sales_revenue as "毛利率= 营业收入-营业成本/营业收入",
(nonbusiness_income-nonbusiness_cost)/total_sales_revenue as "营业外收入-营业外支出 /营业总收入",
sales_profit/sales_revenue as "营业利润率=营业利润/营业收入"
from lrb INNER JOIN xjllb on xjllb.report_date=lrb.report_date and xjllb.sh_code=lrb.sh_code  WHERE lrb.sh_code='600009';




SELECT xjllb.report_date,
net_sale_profit as "经营活动现金流净额",
net_sale_profit/(zcfzb.should_pay_notes+zcfzb.should_pay_account+zcfzb.other_should_pay_account) as "经营活动现金流净额幅度/应付的钱幅度",
(selling_income_cash+selling_corop_income)/investment_total as "投资活动现金流情况",
financing_in/financing_out as "取得借款收到的现金/偿还债务支付的现金",
cash_add as "现金及现金等价物的净增加额"
from xjllb INNER JOIN zcfzb on zcfzb.report_date=xjllb.report_date and xjllb.sh_code=zcfzb.sh_code  WHERE xjllb.sh_code='600009';



--|资产成分|如果占比很大，公司很可能不务正业| 非主业资产/总资产|报表暂时无法分析这条|

