import _thread
import time
count = 0
# 为线程定义一个函数
def print_time( threadName, delay):
   global count
   while count < 10:
      time.sleep(1)
      count += 1


# 创建两个线程
try:
    _thread.start_new_thread( print_time, ("Thread-1", 2, ))
    while(count < 3):
        print("run")
    print(count)
except:
   print ("Error: 无法启动线程")

while 1:
   pass