
import os
import random
import socket
import traceback
import tensorflow as tf
import NNModel.Config as config
import NNModel.DisplayNetwork as DisplayNetwork
root = os.path.dirname(__file__)
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("connected")
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': "Add Connection"
        }))
        self.run_live()


    def run_live(self):
        self.send(text_data=json.dumps({
            'message': "Connecting"
        }))
        data = config.get_data(training=False)
        model = config.get_model(data, training=False)
        global_step = tf.contrib.framework.get_or_create_global_step()
        saver = tf.train.Saver()
        with tf.Session() as session:
            print("NNModel\\" + config.get_checkpoint_dir() + '\\')
            checkpoint = tf.train.latest_checkpoint(root + "\\NNModel\\" + config.get_checkpoint_dir() + '\\')
            if checkpoint == None:
                raise Exception("No checkpoint found.")
            else:
                parts = checkpoint.split("-")
                parts[-1] = "86139"
                checkpoint = "-".join(parts)
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
            port = 2222
            server.bind((socket.gethostname(), port))
            print("Hostname: %s Port: %d" % (socket.gethostname(), port))
            server.listen(1)
            while True:
                print("Listening for connection on port %d..." % (port,))
                (clientsocket, address) = server.accept()
                print("Received client at %s" % (address,))
                # self.send(text_data=json.dumps({
                #     'message': data
                # }))
                display = DisplayNetwork.Display(data.input_width, data.input_height)
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
                        self.send(text_data=json.dumps({
                            'message': str(single_input[0])
                        }))
                        display.update(single_input[0], state, prediction[0])
                except:
                    print("Exception occurred. Closing connection.")
                    print(traceback.print_exc())
                    clientsocket.send(b"close")
                    clientsocket.close()
                finally:
                    display.close()
