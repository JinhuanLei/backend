# Create your views here.
from django.shortcuts import render
import json
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def time(request):
    time = "2018-11-30"
    return HttpResponse(json.dumps(time), content_type='application/json')
