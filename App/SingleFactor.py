# -*- coding:utf-8 -*-
import pymysql
import numpy as np
import pandas as pd


class SingleFactor:
    def __init__(self):
        db_server = "172.16.63.60"  # 连接服务器地址
        user = "root"  # 连接帐号
        password = "lgmysql@"  # 连接密码
        self.__conn = pymysql.connect(host=db_server, port=3306, user=user, passwd=password, db="stock_data",
                                      charset='utf8')
        self.__cursor = self.__conn.cursor()
        print('连接到mysql服务器...')

    def get_data(self, sh_code):
        sql_select = ('''
        select market_date,volume from stock 
             WHERE sh_code='%s';
        ''' % (sh_code))
        self.__cursor.execute(sql_select)
        # 获取所有记录列表
        result = self.__cursor.fetchall()
        vpd = pd.DataFrame(list(result), columns=['date', 'volume'])
        # print vpd.head()
        return vpd


def convert_to_int(ele):
    return int(ele)


if __name__ == '__main__':
    sFact = SingleFactor()
    vpd = sFact.get_data('600010')
    vpd['volume']=vpd['volume'].astype(int)
    ax= vpd.hist()
