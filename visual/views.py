# Create your views here.
import json
import time

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from visual.models import NeuralNetworkModel, Layer, Config
from .Job import Job

task = None


def quickStart(request):

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


def testFunc(request):
    global task
    if task is None:
        task = Job()
        task.start()
    if task.isRuning():
        task.pause()
        print("Pause the Tasks")
    else:
        task.resume()
        print("resume the Tasks")
    return HttpResponse()


def testDB(request):
    fruit = Fruit.objects.create(name='Apple')
    fruit.save()
    return HttpResponse()
