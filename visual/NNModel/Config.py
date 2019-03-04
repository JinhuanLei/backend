import configparser
import os

from MarioRNN import MarioRNN
from TrainData import DataSet

root = os.path.dirname(__file__)
configFilename = root + "/server_defaults.cfg"
config = configparser.ConfigParser()
config.read(["defaults.cfg", configFilename])
if __name__ == "__main__":
    print(config.get("Data", "Filename").strip().split('\n'))

def get_data(training):
    data = DataSet(
        filenames=config.get("Data", "Filename").strip().split('\n'),
        sequence_len=int(config.get("Data", "SequenceLength")),
        batch_size=int(config.get("Data", "BatchSize")),
        train=training,
        num_passes=int(config.get("Train", "NumPasses")),
        recur_buttons=config.get("Data", "RecurButtons") == "True"
    )

    return data


def builtLayer():
    rnn_sizes = []
    layer = 1
    while True:
        try:
            size = int(config.get("RNN", "Layer" + str(layer)))
            if size < 1:
                break
            rnn_sizes.append(size)
            layer = layer + 1
        except:
            break
    print("RNN Sizes: " + str(rnn_sizes))
    return rnn_sizes


def get_model(data, training):
    rnn_sizes = builtLayer()
    model = MarioRNN(
        data=data,
        rnn_sizes=rnn_sizes,
        max_grad_norm=float(config.get("Train", "MaxGradNorm")),
        dropout_keep=float(config.get("Train", "DropoutKeep")),
        variational_recurrent=config.get("Train", "VariationalRecurrent") == "True",
        train=training,
        loss_function=config.get("Train", "LossFunction")
    )

    return model


def get_checkpoint_dir():
    print("configPath", config.get("Checkpoint", "Dir"))
    return config.get("Checkpoint", "Dir")


def get_validation_period():
    return float(config.get("Train", "ValidationPeriod"))
