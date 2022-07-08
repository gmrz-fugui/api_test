# import matplotlib.pyplot as plt
#
# x_values = list(range(10))
# # x轴的数字是0到10这11个整数
# y_values = list(range(10))
# print(y_values)
# # y轴的数字是x轴数字的平方
# plt.plot(x_values, y_values, c = 'green')
# # 用plot函数绘制折线图，线条颜色设置为绿色
# plt.title('Squares', fontsize = 24)
# # 设置图表标题和标题字号
# plt.tick_params(axis = 'both', which = 'major', labelsize = 10)
# # 设置刻度的字号
# # plt.xlabel('Numbers', fontsize = 2)
# # 设置x轴标签及其字号
# # plt.ylabel('Squares', fontsize = 2)
# # 设置y轴标签及其字号
# plt.show()
# # 显示图表

import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

# 从pyplot导入MultipleLocator类，这个类用于设置刻度间隔

x_values = list(range(11))
y_values = [ x ** 2 for x in x_values ]
plt.plot(x_values, y_values, c = 'green')
plt.title('Squares', fontsize = 24)
plt.tick_params(axis = 'both', which = 'major', labelsize = 8)
plt.xlabel('Numbers', fontsize = 14)
plt.ylabel('Squares', fontsize = 14)
x_major_locator = MultipleLocator(1)
# 把x轴的刻度间隔设置为1，并存在变量里
y_major_locator = MultipleLocator(10)
# 把y轴的刻度间隔设置为10，并存在变量里
ax = plt.gca()
# ax为两条坐标轴的实例
ax.xaxis.set_major_locator(x_major_locator)
# 把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator)
# 把y轴的主刻度设置为10的倍数
plt.xlim(-0.5, 11)
# 把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
plt.ylim(-5, 110)
# 把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白
plt.show()
