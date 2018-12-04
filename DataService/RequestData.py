# -*- coding:utf-8 -*-

import requests
import re
from lxml import etree
import time
from DownloadData import Download_HistoryStock


class StockCode(object):
    def __init__(self):
        self.start_url = "http://quote.eastmoney.com/stocklist.html#sh"
        self.headers = {
            "User-Agent": ":Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }

    def parse_url(self):
        # 发起请求，获取响应
        response = requests.get(self.start_url, headers=self.headers)
        if response.status_code == 200:
            return etree.HTML(response.content)

    def get_code_list(self, response):
        # 得到股票代码的列表
        node_list = response.xpath('//*[@id="quotesearch"]/ul[1]/li')
        code_list = []
        for node in node_list:
            try:
                code = re.match(r'.*?\((\d+)\)', etree.tostring(node).decode()).group(1)
                # print code
                code_list.append(code)
            except:
                continue
        return code_list

    def run(self):
        html = self.parse_url()
        return self.get_code_list(html)


if __name__ == '__main__':
    code = StockCode()
    code_list = code.run()
    code_remove = []
    for code in code_list:
        if str(code).startswith("2") or str(code).startswith("5"):
            code_remove.append(code)
    related_code = [v for v in code_list if v not in code_remove]

    for temp_code in code_list:
        time.sleep(2)
        download = Download_HistoryStock(temp_code)
        download.run()
