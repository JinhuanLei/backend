# Create your views here.
import json
import sys
import time

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from visual.models import NeuralNetworkModel, Layer, Config

sys.path.append('/visual/NNModel')
import Train
task = None


def startTraining(request, id):
    layers = list(Layer.objects.filter(model_id=id).values())
    training_layer = []
    print(layers)
    for layer in layers:
        training_layer.append(layer['num_nets'])
    Train.train(True, training_layer)
    return HttpResponse(json.dumps(""), content_type='application/json')


def stopTraining(request, id):
    Train.pause()
    return HttpResponse(json.dumps(""), content_type='application/json')


def getModelById(request, id):
    print(id)
    # model = list(NeuralNetworkModel.objects.get(id=id))
    layers = list(Layer.objects.filter(model_id=id).values())
    print(layers)
    return HttpResponse(json.dumps(layers), content_type='application/json')


def quickStart(request):
    nnmodel = NeuralNetworkModel.objects.create(model_name='Default Model', model_duration=0)
    model_id = nnmodel.id
    nnmodel.save()
    config = Config.objects.create(dropout_rate=0.5, num_passes=10, model_id=model_id)
    print(config.id)
    config_id = config.id
    config.save()
    reqLayers = defaultConfig.builtLayer()
    for l in reqLayers:
        layer = Layer.objects.create(config_id=config_id, num_nets=l, model_id=model_id)
        layer.save()
    return HttpResponse(json.dumps("return this string"))


@csrf_exempt
def createModel(request):
    received_json_data = json.loads(request.body)
    print(received_json_data)
    nnmodel = NeuralNetworkModel.objects.create(model_name=received_json_data['model_name'], model_duration=0)
    model_id = nnmodel.id
    nnmodel.save()
    config = Config.objects.create(dropout_rate=0.5, num_passes=10, model_id=model_id)
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
    # print(models)
    # for model in models:
    #     print(model.id)
    # data = serializers.serialize('json', models)
    return HttpResponse(json.dumps(models), content_type='application/json')


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
