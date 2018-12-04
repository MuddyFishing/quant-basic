# -*- coding:utf-8 -*-
import csv

import os
import sys
import pymysql
import pandas as pd
import numpy as np


# 导入历史交易数据
class DataService:
    def __init__(self):
        db_server = "172.16.63.60"  # 连接服务器地址
        user = "root"  # 连接帐号
        password = "lgmysql@"  # 连接密码
        self.__conn = pymysql.connect(host=db_server, port=3306, user=user, passwd=password, db="stock_data",
                                      charset='utf8')
        self.__cursor = self.__conn.cursor()
        print('连接到mysql服务器...')
        self.__dirName = "G:\\stock_data\\lsjysj"
        self.__dirNameOfLrb = "G:\\stock_data\\lrb"
        self.__dirNameOfXjllb = "G:\\stock_data\\xjllb"
        self.__dirNameOfZcfzb = "G:\\stock_data\\zcfzb"

    def get_dir_filename(self, file_dir):
        '获取目录下的所有的文件名'
        for root, dirs, files in os.walk(file_dir):
            # print(root)  # 当前目录路径
            # print(dirs)  # 当前路径下所有子目录
            return files  # 当前路径下所有非目录子文件

    def format_float(self, val):
        '浮动数格式化'
        if val is None or str(val).strip() == '' or str(val).__contains__("None") or str(val).__contains__("--"):
            return 0.0
        else:
            try:
                return float(val)
            except:
                print val + "sddd"

    def truncate_db(self, table):
        insert_sql = "TRUNCATE TABLE  `" + table + "`;"
        self.__cursor.execute(insert_sql)
        self.__conn.commit()

    def close_conn(self):
        self.__conn.close()

    def insert_db(self):
        '写入数据到历史交易数据表'
        self.truncate_db("stock")
        files = self.get_dir_filename(self.__dirName)
        for file in files:
            print "writing file...and filename is :" + file

            csv_reader = csv.reader(open(self.__dirName + r'\\'.decode() + file))
            list_tuple = []
            # 读取每一个文件的数据，并写入到数据库
            for row in csv_reader:
                date = row[0].decode("gb2312")
                # 如果是第一行数据，跳过
                if (date.encode("utf-8")).__contains__("日期") or str(row[14]).__contains__('e'):
                    continue
                else:
                    values_tuple = (
                        date.encode("utf-8"), (row[1])[1:], (row[2].decode("gb2312")).encode("utf-8"),
                        self.format_float(row[3]), self.format_float(row[4]), self.format_float(row[5]),
                        self.format_float(row[6]), self.format_float(row[7]), self.format_float(row[8]),
                        self.format_float(row[9]), self.format_float(row[10]), self.format_float(row[11]),
                        self.format_float(row[12]), self.format_float(row[13]), self.format_float(row[14]))
                    list_tuple.append(values_tuple)

            insert_sql = "INSERT INTO stock(market_date,sh_code,sh_name,price_close,price_high,price_low,price_open,price_pre_open,change_val,chg,turnover_rate,volume,turnover,market_cap,flow_market_cap) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.__cursor.executemany(insert_sql, list_tuple)
            self.__conn.commit()
            print "**************writing lsjysj file :" + file + " --finished*************** :"

    def insert_lrb(self):
        '写入数据到利润表'

        self.truncate_db("lrb")
        files = self.get_dir_filename(self.__dirNameOfLrb)
        for file in files:
            data = pd.read_csv(self.__dirNameOfLrb + r'\\'.decode() + file)
            if data.shape[0] <= 1:
                continue
            sh_code = file[:-4]
            list_tuple = []
            for date_index, row in data.T.iterrows():
                # date= report_dates[index]
                if ("报告日期" in date_index.decode("gb2312").encode("utf-8")) or (
                            "Unnamed" in date_index.decode("gb2312").encode("utf-8")) or date_index.strip()=='':
                    continue

                else:
                    row_vals = row.tolist()
                    row_vals = [self.format_float(item) for item in row_vals]
                    values_tuple = (
                        date_index, sh_code, row_vals[0], row_vals[1], row_vals[7], row_vals[8],
                        row_vals[32], row_vals[33], row_vals[34], row_vals[39], row_vals[43], row_vals[44])
                    list_tuple.append(values_tuple)
            insert_sql = "INSERT INTO lrb(report_date,sh_code,total_sales_revenue,sales_revenue,total_operation_cost,operation_cost,sales_profit,nonbusiness_income,nonbusiness_cost,net_profit,earning_per_sharing,ex_earning_per_sharing) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.__cursor.executemany(insert_sql, list_tuple)
            self.__conn.commit()
            print "**************writing lrb file :" + file + " --finished*************** :"

    def insert_xjllb(self):
        '写入数据到现金流量表'
        self.truncate_db("xjllb")
        files = self.get_dir_filename(self.__dirNameOfXjllb)
        for file in files:
            data = pd.read_csv(self.__dirNameOfXjllb + r'\\'.decode() + file)
            if data.shape[0] <= 1:
                continue
            sh_code = file[:-4]
            list_tuple = []
            for date_index, row in data.T.iterrows():
                if ("报告日期" in date_index.decode("gb2312").encode("utf-8")) or (
                            "Unnamed" in date_index.decode("gb2312").encode("utf-8")) or date_index.strip()=='':
                    continue

                else:
                    row_vals = row.tolist()
                    row_vals = [self.format_float(item) for item in row_vals]
                    values_tuple = (
                        date_index.strip(), sh_code, row_vals[0], row_vals[24], row_vals[27], row_vals[28],
                        row_vals[32], row_vals[39], row_vals[42]
                        , row_vals[46], row_vals[51], row_vals[53])
                    list_tuple.append(values_tuple)
            insert_sql = "INSERT INTO xjllb(report_date,sh_code,sale_or_work_income,net_sale_profit,selling_income_cash,selling_corop_income,shoping_out_cash,investment_total,financing_in,financing_out,financing_total,cash_add) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.__cursor.executemany(insert_sql, list_tuple)
            self.__conn.commit()
            print "**************writing xjllb file :" + file + " --finished*************** :"

    def insert_zcfzb(self):
        '写入资产负债表'
        self.truncate_db("zcfzb")
        files = self.get_dir_filename(self.__dirNameOfZcfzb)
        for file in files:
            data = pd.read_csv(self.__dirNameOfZcfzb + r'\\'.decode() + file)
            if data.shape[0] <= 1:
                continue
            sh_code = file[:-4]
            list_tuple = []
            for date_index, row in data.T.iterrows():
                if ("报告日期" in date_index.decode("gb2312").encode("utf-8")) or (
                            "Unnamed" in date_index.decode("gb2312").encode("utf-8")) or date_index.strip()=='':
                    continue

                else:
                    row_vals = row.tolist()
                    row_vals = [self.format_float(item) for item in row_vals]
                    values_tuple = (
                        date_index.strip(), sh_code,
                        row_vals[0], row_vals[5], row_vals[6], row_vals[7], row_vals[13], row_vals[19], row_vals[23]
                        , row_vals[24], row_vals[36], row_vals[37], row_vals[31], row_vals[46], row_vals[49],
                        row_vals[50], row_vals[51], row_vals[52], row_vals[58], row_vals[59], row_vals[70],row_vals[82], row_vals[83]
                        , row_vals[84],row_vals[91], row_vals[92], row_vals[93]
                        , row_vals[101], row_vals[106], row_vals[107])

                    list_tuple.append(values_tuple)

            insert_sql = "INSERT INTO zcfzb(report_date,sh_code,monetary_resources,notes_receivable,accounts_receivable,prepayments,others_accounts_receivable,inventory,other_flow_assert,flow_assert,fixed_assets,uncompleted_construction,investment_real_estate,long_pre_ability,other_non_flow_assert,non_flow_assert,assert_total,short_term_liability,should_pay_notes,should_pay_account,other_should_pay_account,other_flow_liabilities,flow_liabilities,long_term_liability,other_non_flow_liabilities,non_flow_liabilities,liabilities_total,undistributed_profit,owners_equity,liabilities_and_equity) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.__cursor.executemany(insert_sql, list_tuple)
            self.__conn.commit()
            print "**************writing zcfzb file :" + file + " --finished*************** :"

if __name__ == '__main__':
    dataService = DataService()
    # dataService .insert_db()
    # dataService.insert_xjllb()
    # dataService.insert_lrb()
    dataService.insert_zcfzb()

    dataService.close_conn()
