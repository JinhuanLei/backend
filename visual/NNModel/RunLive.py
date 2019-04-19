import os
import random
import socket
import traceback

import tensorflow as tf
from visual.models import Config
import CostomiseModel as cm
import DisplayNetwork

# data = config.get_data(training=False)
# model = config.get_model(data, training=False)
# global_step = tf.contrib.framework.get_or_create_global_step()  # old one already deprecated
# global_step = tf.train.get_or_create_global_step()
keepConnecting = True
clientsocket = None
server = None


def disconnect():
    global keepConnecting
    keepConnecting = False


def connect():
    global keepConnecting
    keepConnecting = True


def runlive(rnn_size, id):
    global keepConnecting, clientsocket, server
    root = os.path.dirname(__file__)
    path = root + '\\trained_model\\' + str(id) + '\\'
    # global data, model, global_step
    global_step = tf.train.get_or_create_global_step()
    # data = config.get_data(training=False)
    # model = config.get_model(data, training=False)
    customizedConfig = list(Config.objects.filter(model_id=id).values())
    data = cm.get_data(customizedConfig[0],training=True)
    model = cm.get_model(customizedConfig[0], data, training=True, rnn_sizes=rnn_size)
    saver = tf.train.Saver()
    with tf.Session() as session:
        checkpoint = tf.train.latest_checkpoint(path)
        if checkpoint is None:
            raise Exception("No checkpoint found.")
        else:
            # if len(sys.argv) >= 3:
            #     parts = checkpoint.split("-")
            #     parts[-1] = sys.argv[2]
            #     checkpoint = "-".join(parts)
            print("Loading {0}".format(checkpoint))
        saver.restore(session, checkpoint)
        state = session.run(model.single_initial_state)
        if data.recur_buttons:
            prev_buttons = [-1] * data.output_size
        else:
            prev_buttons = []

        fetches = {
            "prediction": model.single_prediction,
            "single_state": model.single_state,
        }

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 这样操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，下次运行就不会出现上述问题啦。
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 2222
        server.bind((socket.gethostname(), port))
        print("Hostname: %s Port: %d" % (socket.gethostname(), port))
        server.listen(1)
        while keepConnecting is True:
            print("Listening for connection on port %d..." % (port,))
            try:
                (clientsocket, address) = server.accept()
            except:
                pass
            if keepConnecting is False:
                print("Break the connecting")
                break
            print("Received client at %s" % (address,))
            # display = DisplayNetwork.Display(data.input_width, data.input_height)
            try:
                clientsocket.send((str(len(data.header)) + "\n").encode())
                for param in data.header:
                    clientsocket.send((str(param) + "\n").encode())
                while True:
                    screen = ""
                    while len(screen) == 0 or screen[-1] != "\n":
                        screen += clientsocket.recv(2048).decode('ascii')
                    screen = screen.strip()
                    words = screen.split(" ")
                    expected_size = data.input_size
                    if data.recur_buttons:
                        expected_size -= data.output_size
                    if len(words) != expected_size:
                        print("Client closed connection.")
                        clientsocket.close()
                        break
                    single_input = [[float(tile) for tile in words] + prev_buttons]
                    feed_dict = {
                        model.single_input: single_input,
                    }
                    for i, (c, h) in enumerate(model.single_initial_state):
                        feed_dict[c] = state[i].c
                        feed_dict[h] = state[i].h
                    values = session.run(fetches, feed_dict)
                    prediction = values["prediction"]
                    state = values["single_state"]
                    buttons = []
                    for p in prediction[0]:
                        if random.random() > p:
                            buttons.append("0")
                        else:
                            buttons.append("1")
                    if data.recur_buttons:
                        prev_buttons = [float(b) for b in buttons]
                    buttons = " ".join(buttons) + "\n"
                    clientsocket.send(buttons.encode())
                    # display.update(single_input[0], state, prediction[0])
            except:
                print("Exception occurred. Closing connection.")
                print(traceback.print_exc())
                clientsocket.send(b"close")
                clientsocket.close()
            finally:
                # display.close()
                print("Close")
    # server.shutdown(socket.SHUT_WR)
    print("RunLive Finished")


def stop_accept():
    # Skip if sock.accept has executed.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if clientsocket is None:
            # ainfo = socket.getaddrinfo('127.0.0.1', 2222)
            # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 2222))
    except:
        print("Error accepted")
        server.close()
        pass


if __name__ == "__main__":
    runlive()
