# Create your views here.
import json
import time

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from visual.models import Fruit, NeuralNetworkModel
from .Job import Job

task = None


@csrf_exempt
def createModel(request):
    received_json_data = json.loads(request.body)
    print(received_json_data)
    nnmodel = NeuralNetworkModel.objects.create(model_name=received_json_data['model_name'], model_period=0)
    nnmodel.save()
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
