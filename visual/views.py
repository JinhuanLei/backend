# Create your views here.
import datetime
import json
import sys
import time

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from visual.models import NeuralNetworkModel, Layer, Config

sys.path.append('/visual/NNModel')
sys.path.append('C:\\Users\\Administrator\\PycharmProjects\\backend\\visual\\NNModel\\')
import RunLive
import Train
import Config as model_config
task = None


def startValidating(request, id):
    layers = list(Layer.objects.filter(model_id=id).values())
    training_layer = []
    print(layers)
    for layer in layers:
        training_layer.append(layer['num_nets'])
    RunLive.connect()
    RunLive.runlive(training_layer, id)
    return HttpResponse(json.dumps(id), content_type='application/json')


def stopValidating(request, id):
    RunLive.disconnect()
    RunLive.stop_accept()
    return HttpResponse(json.dumps(id), content_type='application/json')


def validateModelById(request, id):
    layers = list(Layer.objects.filter(model_id=id).values())
    training_layer = []
    print(layers)
    for layer in layers:
        training_layer.append(layer['num_nets'])
    RunLive.runlive(training_layer, id)
    return HttpResponse(json.dumps(id), content_type='application/json')


def deleteModelById(request, id):
    Layer.objects.filter(model_id=id).delete()
    Config.objects.filter(model_id=id).delete()
    NeuralNetworkModel.objects.filter(id=id).delete()
    return HttpResponse(json.dumps(id), content_type='application/json')

@csrf_exempt
def updateTrainingPeriod(request, id):
    received_json_data = json.loads(request.body)
    trained_time = received_json_data['training_period_inc']
    # layers = list(Layer.objects.filter(model_id=id).values())
    neuralNetwork = NeuralNetworkModel.objects.get(id=id)
    model_duration = neuralNetwork.model_duration
    result = model_duration + trained_time
    print(result)
    neuralNetwork.model_duration = result
    neuralNetwork.save()
    return HttpResponse(json.dumps(id), content_type='application/json')


def startTraining(request, id):
    layers = list(Layer.objects.filter(model_id=id).values())
    training_layer = []
    print(layers)
    for layer in layers:
        training_layer.append(layer['num_nets'])
    Train.start()
    Train.train(True, training_layer, id)
    return HttpResponse(json.dumps(""), content_type='application/json')


def stopTraining(request, id):
    Train.pause()
    return HttpResponse(json.dumps(""), content_type='application/json')


def getModelById(request, id):
    print(id)
    training_set = NeuralNetworkModel.objects.get(id=id).training_set
    layers = list(Layer.objects.filter(model_id=id).values())
    config = list(Config.objects.filter(model_id=id).values())
    print(layers)
    data = {'training_set': training_set, 'layers': layers, 'config': config}
    return HttpResponse(json.dumps(data), content_type='application/json')


def quickStart(request):
    nnmodel = NeuralNetworkModel.objects.create(model_name='Default Model', model_duration=0, training_set="Default")
    model_id = nnmodel.id
    nnmodel.save()
    config = Config.objects.create(drop_out=0.5,
                                   num_passes=10,
                                   batch_size=3,
                                   sequence_length=20,
                                   loss_function="Mean Squared Error",
                                   recur_button=True,
                                   max_grad=10,
                                   variational_recurrent=True,
                                   model_id=model_id)
    print(config.id)
    config_id = config.id
    config.save()
    reqLayers = model_config.builtLayer()
    for l in reqLayers:
        layer = Layer.objects.create(config_id=config_id, num_nets=l, model_id=model_id)
        layer.save()
    return HttpResponse(json.dumps("return this string"))


@csrf_exempt
def createModel(request):
    received_json_data = json.loads(request.body)
    print(received_json_data)
    nnmodel = NeuralNetworkModel.objects.create(model_name=received_json_data['model_name'], model_duration=0, training_set=received_json_data['trainingSet'])
    model_id = nnmodel.id
    nnmodel.save()

    config = Config.objects.create(drop_out=received_json_data['dropOut'],
                                   batch_size=received_json_data['batchSize'],
                                   sequence_length=received_json_data['sequenceLength'],
                                   num_passes=10,
                                   model_id=model_id,
                                   loss_function=received_json_data['lossFunction'],
                                   recur_button=False,
                                   max_grad=10,
                                   variational_recurrent=True
                                   )
    print(config.id)
    config_id = config.id
    config.save()
    reqLayers = received_json_data['layers']
    for l in reqLayers:
        layer = Layer.objects.create(config_id=config_id, num_nets=l['val'], model_id=model_id)
        layer.save()
    return HttpResponse(json.dumps(received_json_data), content_type='application/json')


def getModels(request):
    models = list(NeuralNetworkModel.objects.all().values())
    # sets = list(TrainingSet.objects.all().values())
    # print(sets)
    # print(models)
    # for model in models:
    #     print(model.id)
    # data = serializers.serialize('json', models)
    return HttpResponse(json.dumps(models, cls=DateEncoder), content_type='application/json')


def index(request):
    return render(request, 'index.html')


def countdown(n):
    while n > 0:
        print('Num', n)
        n -= 1
        time.sleep(2)


flag = True


def testFunc(request):
    global flag
    flag = True
    # global task
    # if task is None:
    #     task = Job()
    #     task.start()
    # if task.isRuning():
    #     task.pause()
    #     print("Pause the Tasks")
    # else:
    #     task.resume()
    #     print("resume the Tasks")
    while flag:
        print("run")
    return HttpResponse()


def testDB(request):
    global flag
    flag = False
    return HttpResponse()


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
