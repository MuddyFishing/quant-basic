# -*- coding:utf-8 -*-
import csv
import sys
import pymysql
import pandas as pd
import numpy as np


class DataService(object):
    def __init__(self):
        db_server = "172.16.63.60"  # 连接服务器地址
        user = "root"  # 连接帐号
        password = "lgmysql@"  # 连接密码
        self.__conn = pymysql.connect(host=db_server, port=3306, user=user, passwd=password, db="stock_data",
                                      charset='utf8')
        self.__cursor = self.__conn.cursor()
        print('连接到mysql服务器...')


    def get_history_data(self, sh_code,start_date,end_date):
        sql_select = ('''
        select market_date,price_open,price_high,price_low from stock 
             WHERE stock.sh_code='%s';
        ''' % (sh_code))
        self.__cursor.execute(sql_select)
        # 获取所有记录列表
        result = self.__cursor.fetchall()
        zcfzb_pd = pd.DataFrame(list(result))

        return zcfzb_pd