from fanancial import FiscalData

fd = FiscalData(ticker='002202')
print(fd.basic_indicator().to_html())
print(fd.basic_assumption().to_html())
print(fd.invest_assumption().to_html())
