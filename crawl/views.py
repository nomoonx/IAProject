from django.shortcuts import render
from django.http import HttpResponse
from .forms import crawlInitForm
from .crawler import crawl_result
import json

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World!")


def index(request):
    form = crawlInitForm(request.POST)
    return render(request, 'index.html', {'crawlForm': form})


def showtime(request):
    param = request.GET['seedHosts']
    hostSeeds = param.split('\n')
    threadNumber = int(request.GET['threadsNumber'])
    maxLength = int(request.GET['maxNumber'])
    jsonResponse = crawl_result(threadNumber, maxLength, hostSeeds)
    return HttpResponse(jsonResponse, content_type="application/json")


def showtime2(request):
    # form=crawlInitForm(request.POST)
    return render(request, 'showtime2.html')


def crawlSite(request):
    hostSeeds = ['microso.me']
    threadNumber = 5
    maxLength = 15
    jsonResponse = crawl_result(threadNumber, maxLength, hostSeeds)
    # return render(request, 'showtime.html', {'hostSeeds': hostSeeds,'threadNumber':threadNumber})
    return HttpResponse(jsonResponse, content_type="application/json")