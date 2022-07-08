
import time
from matplotlib import pyplot as plt
from testFile import remote_host
import re

top = remote_host.host_command().run("top -n 1 -b -p 0",hide = True).stdout
# cpu = top[145:225]
print(top)
# print(cpu)
# print(re.findall(r"\d+\.?\d*", cpu))

used = []
t = []

for i in range(10):
    print(i)
    t1=time_now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    output = remote_host.host_command().run('top -n 1 -b -p 0', hide = True).stdout
    cpu = output[ 145:225 ]
    d = re.findall(r"\d+\.?\d*", cpu)
    used.append(float(d[1]))
    t.append(t1)

    plt.plot(t, used,color='red')
    plt.xlabel('time', fontsize = 10) # 横坐标文字和字体大小
    plt.ylabel('use memory (mb)', fontsize = 10) # 纵坐标文字和文字大小
    plt.ylim(0, 1) # 纵坐标最大值和最小值
    plt.xticks(rotation = 90) # 横坐标时间竖着显示，360为横着显示

    plt.show()
    time.sleep(1)
