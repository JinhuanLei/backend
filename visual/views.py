# Create your views here.
import json
import time
from django.http import HttpResponse
from django.shortcuts import render
from Job import Job
task = None


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
    return HttpResponse(json.dumps(""), content_type='application/json')
