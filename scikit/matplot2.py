# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
#
# # 从[-1,1]中等距去50个数作为x的取值
# x = np.linspace(-1, 1, 50)
# y1 = 2*x + 1
# y2 = 2**x + 1
#
# # 第一个参数表示的是编号，第二个表示的是图表的长宽
# plt.figure(num = 3, figsize=(8, 5))
# plt.plot(x, y2)
# plt.plot(x, y1, color='red', linewidth=1.0, linestyle='--')
#
# # 设置取值参数
# plt.xlim((-1, 2))
# plt.ylim((1, 3))
#
#
#
# # 设置点的位置
# new_ticks = np.linspace(-1, 2, 5)
# plt.xticks(new_ticks)
# plt.yticks([-2, -1.8, -1, 1.22,3],
#           [r'$really\ bad$', r'$bad$', r'$normal$', r'$good$', r'$readly\ good$'])
#
#
# l1, = plt.plot(x, y2,
#                label='aaa'
#               )
# l2, = plt.plot(x, y1,
#                color='red',  # 线条颜色
#                linewidth = 1.0,  # 线条宽度
#                linestyle='-.',  # 线条样式
#                label='bbb'  #标签
#               )
#
# plt.legend(
#     handles=[l1,l2],
#     labels=['aaa','bbb'],
#     loc='best'
# )
#
# ax = plt.gca()
# # 将右边和上边的边框（脊）的颜色去掉
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
#


#figure3
n=12
X=np.arange(n)
Y1= (1-X/float(n))*np.random.uniform(0.5,1.0,n)
Y2= (1-X/float(n))*np.random.uniform(0.5,1.0,n)

plt.figure(num=3,figsize=(12,8))
plt.bar(X,Y1,facecolor='#9999ff', edgecolor='white')
# plt.xlim(0,n)
# plt.xticks()



plt.show()
