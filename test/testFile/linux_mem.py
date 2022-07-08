from testFile import remote_host
import re
import time
from matplotlib import pyplot as plt



used = []
t = []

for i in range(10):
    print(i)
    t1=time_now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    output = remote_host.host_command().run('freed -m', hide = True).stdout

    me = output[ 90:130 ]
    d = re.findall(r"\d+\.?\d*", me)
    used.append(int(d[1]))
    t.append(t1)

    plt.plot(t, used,color='green')
    plt.xlabel('time', fontsize = 10) # 横坐标文字和字体大小
    plt.ylabel('use memory (mb)', fontsize = 10) # 纵坐标文字和文字大小
    plt.ylim(1000, 16000) # 纵坐标最大值和最小值
    plt.xticks(rotation = 90) # 横坐标时间竖着显示，360为横着显示


    # if len(used)>3:
    #     used.pop(0)
    #     t.pop(0)

    # # x = np.linspace(-1, 1, 30)  # 从(-1,1)均匀取50个点
    # # y = 2 * x
    #
    # plt.plot(used,color='green')


    plt.show()
    time.sleep(1)
