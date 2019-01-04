# -*- coding:utf-8 -*-

import numpy as np
import talib
import pandas as pd
from DataService import DataInterface
from matplotlib import pyplot as plt

PARAMAS = {
    "start_time": "2016-10-01 00:00:00",
    "end_time": "2017-07-01 00:00:00",
    "commission_ratio": 0.0003,  # 此处设置交易佣金
    "slippage": 0.001,  # 此处设置交易滑点
    "cny_cash": 10000
}


def initialize(context):
    # 设置回测频率, 可选："1m", "5m", "15m", "30m", "60m", "4h", "1d", "1w"
    adx_period = 12
    dmi_period = 12
    ma_short_period = 5
    ma_long_period = 5


# def compute_DM(pd):
#     talib.

def talib_func():
    # sma = abstract.Function('sma')
    close = np.random.random(30)
    # print close
    output = talib.SMA(close, 5)
    print output
    (upper, middle, lower) = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=3)
    # print (upper, middle, lower)
    # output = talib.MOM(close, timeperiod=5)
    # print output
    price = DataInterface().get_price('600010', '2018-01-01', '2018-09-01')
    ppd = pd.DataFrame(list(price), columns=['tdate', 'price_open', 'price_close', 'price_high', 'price_low'])
    low = ppd['price_low'].apply(pd.to_numeric)
    # low=low.where(low>0)
    high = ppd['price_high'].apply(pd.to_numeric)
    # high = high.where(high > 0)
    open = ppd['price_open'].apply(pd.to_numeric)
    close = ppd['price_close'].apply(pd.to_numeric)
    minus_di = talib.MINUS_DI(high.values, low.values, close.values, timeperiod=5)
    plus_di = talib.PLUS_DI(high.values, low.values, close.values, timeperiod=5)

    # print low
    # real = talib.SAR(high, low, acceleration=0, maximum=0)
    real = talib.ATR(high, low, close, timeperiod=14)
    real = talib.CDLEVENINGSTAR(open, high, low, close, penetration=0)
    plt.plot(real)
    plt.show()


def strategy_handle(context):
    data = DataInterface()
    hist = data.get_price("", "", "")


talib_func()
