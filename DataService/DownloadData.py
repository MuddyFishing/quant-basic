# -*- coding:utf-8 -*-
import requests
import re
from lxml import etree
import xml.etree
import codecs


class Download_HistoryStock(object):
    def __init__(self, code):
        self.code = code
        self.start_url = "http://quotes.money.163.com/trade/lsjysj_" + self.code + ".html"
        print self.start_url
        self.headers = {
            "User-Agent": ":Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }

    def parse_url(self):

        response = requests.get(self.start_url)
        # print response.status_code
        if response.status_code == 200:
            return etree.HTML(response.content)
        return False

    def get_date(self, response):
        # 得到开始和结束的日期
        start_date = ''.join(response.xpath('//input[@name="date_start_type"]/@value')[0].split('-'))
        end_date = ''.join(response.xpath('//input[@name="date_end_type"]/@value')[0].split('-'))
        return start_date, end_date

    def download(self, start_date, end_date):
        download_url = "http://quotes.money.163.com/service/chddata.html?code=0" + self.code + "&start=" + start_date + "&end=" + end_date + "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        data = requests.get(download_url)
        f = open(r"G:\\stock_data\\lsjysj\\" + self.code + '.csv', 'wb')
        for chunk in data.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
        print '股票---', self.code, '历史数据正在下载'

    # 资产负债表
    def download_zcfzb_report(self):
        download_url = "http://quotes.money.163.com/service/zcfzb_" + self.code + ".html"
        report = requests.get(download_url)
        f = open(r"G:\\stock_data\\zcfzb\\" + self.code + '.csv', 'wb')
        for chunk in report.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
        print '资产负债表---', self.code, '数据正在下载'

    # 利润表
    def download_lrb_report(self):
        download_url = "http://quotes.money.163.com/service/lrb_" + self.code + ".html"
        report = requests.get(download_url)
        f = open(r"G:\\stock_data\\lrb\\" + self.code + '.csv', 'wb')
        for chunk in report.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
        print '利润表---', self.code, '数据正在下载'

    # 现金流量表
    def download_xjllb_report(self):
        download_url = "http://quotes.money.163.com/service/xjllb_" + self.code + ".html"
        report = requests.get(download_url)
        f = open(r"G:\\stock_data\\xjllb\\" + self.code + '.csv', 'wb')
        for chunk in report.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
        print '现金流量表---', self.code, '数据正在下载'

    def run(self):
        try:
            html = self.parse_url()
            if html:
                start_date, end_date = self.get_date(html)
                self.download(start_date, end_date)
            self.download_zcfzb_report()
            self.download_lrb_report()
            self.download_xjllb_report()
        except Exception as e:
            print e
