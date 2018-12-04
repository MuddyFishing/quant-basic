# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-1, 1, 50)
y1 = 2 * x + 1
y2 = 2 ** x + 1
#
# plt.figure()
# plt.plot(x, y1)
# plt.plot(x, y2)


plt.figure()
plt.plot(x,y2)
plt.plot(x,y1,color='red',linewidth=1.0,linestyle='--')
plt.xlabel("x")
plt.ylabel("y")
plt.xlim((-2,2))
plt.ylim((-1,5))

#设置坐标轴点的位置
# new_ticks = np.linspace(-2,2,5)
# plt.xticks(new_ticks)
#
# plt.yticks([-2, -1.8, -1, 1.22, 3],
#           [r'$really\ bad$', r'$bad$', r'$normal$', r'$good$', r'$readly\ good$'])

# gca = 'get current axis'
ax = plt.gca()
# 将右边和上边的边框（脊）的颜色去掉
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 绑定x轴和y轴
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
# 定义x轴和y轴的位置
ax.spines['bottom'].set_position(('data', 1))
ax.spines['left'].set_position(('data', 0))
plt.show()
