from MarioRNN import MarioRNN
from TrainData import DataSet
import configparser
import os
root = os.path.dirname(__file__)
configFilename = root + "/server_defaults.cfg"
config = configparser.ConfigParser()
config.read(["defaults.cfg", configFilename])

def get_data(training):
    data = DataSet(
        filenames=['data\\TiltedFixed2.txt'],
        sequence_len=20,
        batch_size=3,
        train=training,
        num_passes=10,
        recur_buttons=False
    )
    return data
# def get_data(training):
#     data = DataSet(
#         filenames=config.get("Data", "Filename").strip().split('\n'),
#         sequence_len=int(config.get("Data", "SequenceLength")),
#         batch_size=int(config.get("Data", "BatchSize")),
#         train=training,
#         num_passes=int(config.get("Train", "NumPasses")),
#         recur_buttons=config.get("Data", "RecurButtons") == "True"
#     )
#
#     return data

def get_model(data, training, rnn_sizes):
    # rnn_sizes = []
    # layer = 1
    # while True:
    #     try:
    #         size = int(config.get("RNN", "Layer" + str(layer)))
    #         if size < 1:
    #             break
    #         rnn_sizes.append(size)
    #         layer = layer + 1
    #     except:
    #         break
    #
    # print("RNN Sizes: " + str(rnn_sizes))

    model = MarioRNN(
        data=data,
        rnn_sizes=rnn_sizes,
        max_grad_norm=float(10),
        dropout_keep=float(0.5),
        variational_recurrent=True,
        train=training,
        loss_function="Mean Squared Error"
    )

    return model
