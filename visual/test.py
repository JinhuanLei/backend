count = 0
# 为线程定义一个函数
# def print_time( threadName, delay):
#    global count
#    while count < 10:
#       time.sleep(1)
#       count += 1
#
#
# # 创建两个线程
# try:
#     _thread.start_new_thread( print_time, ("Thread-1", 2, ))
#     while(count < 3):
#         print("run")
#     print(count)
# except:
#    print ("Error: 无法启动线程")
#
# while 1:
#    pass
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# port = 2333
# server.bind((socket.gethostname(), port))
# print("Hostname: %s Port: %d" % (socket.gethostname(), port))
# server.listen(1)
# print("Listening for connection on port %d..." % (port,))
# (clientsocket, address) = server.accept()
# print("I am here")
import os, pickle
root = os.path.dirname(__file__)
object_path = root + '/NNModel/loaded_object/' + '1/'
if not os.path.isdir(object_path):
            os.makedirs(object_path)
data = {"233": 233}
with open(object_path + 'test.txt', 'wb') as f:
    pickle.dump(data, f)