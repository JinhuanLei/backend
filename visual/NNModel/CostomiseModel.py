from MarioRNN import MarioRNN
from TrainData import DataSet
import configparser
import os
root = os.path.dirname(__file__)
configFilename = root + "/server_defaults.cfg"
config = configparser.ConfigParser()
config.read(["defaults.cfg", configFilename])

def get_data(customizedConfig,training_set, training):
    # filenames=['data\\TiltedFixed2.txt'],
    print(customizedConfig)
    data = DataSet(
        filenames=['data\\'+training_set+'.txt'],
        sequence_len=customizedConfig['sequence_length'],
        batch_size=customizedConfig['batch_size'],
        train=training,
        num_passes=customizedConfig['num_passes'],
        recur_buttons=customizedConfig['recur_button'],
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

def get_model(customizedConfig,data, training, rnn_sizes):
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
        max_grad_norm=float(customizedConfig['max_grad']),
        dropout_keep=float(customizedConfig['drop_out']),
        variational_recurrent=customizedConfig['variational_recurrent'],
        train=training,
        loss_function=customizedConfig['loss_function']
    )

    return model
