# -*- coding:utf-8 -*-
import pymysql
import numpy as np
import pandas as pd


class AppService:
    def __init__(self):
        db_server = "172.16.63.60"  # 连接服务器地址
        user = "root"  # 连接帐号
        password = "lgmysql@"  # 连接密码
        self.__conn = pymysql.connect(host=db_server, port=3306, user=user, passwd=password, db="stock_data",
                                      charset='utf8')
        self.__cursor = self.__conn.cursor()
        print('连接到mysql服务器...')

    # def get_recent_date(self):
    #     select_data = "select report_date from zcfzb order by report_date DESC limit 1;"
    #     self.__cursor.execute(select_data)
    #     date = self.__cursor.fetchone()
    #     print date

    def get_data(self, sh_code):
        sql_select = ('''
        select * from zcfzb 
             WHERE zcfzb.sh_code='%s';
        ''' % (sh_code))
        self.__cursor.execute(sql_select)
        # 获取所有记录列表
        result = self.__cursor.fetchall()
        zcfzb_pd = pd.DataFrame(list(result))
        del zcfzb_pd[0]
        del zcfzb_pd[2]
        return zcfzb_pd

    def get_inditor(self, sh_code):
        inditor_df= pd.DataFrame()
        zcfzb_df = self.get_data(sh_code)
        inditor_df['b1']= (zcfzb_df[3]-zcfzb_df[5])/zcfzb_df[3]
        inditor_df['margin2']= (zcfzb_df[6]-zcfzb_df[3])
        return inditor_df


if __name__ == '__main__':
    app = AppService()
    inditor=app.get_inditor("600009")
    print inditor.to_html()
