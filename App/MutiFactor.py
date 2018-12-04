# -*- coding:utf-8 -*-
import pymysql
import numpy as np
import pandas as pd
import talib
import scipy.stats as st
factor1 = pd.concat([pd.DataFrame(np.random.random((300, 3))), pd.DataFrame(np.ones((300, 3))*[0.5, 0.3, 0.2])], axis=1).loc[:, [0,1,2]]
factor1.columns = ['因子1', '权重1', '因子2', '权重2','因子3', '权重3']

factor1['日期'] = '20181229'
print factor1.pivot
