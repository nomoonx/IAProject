from django.shortcuts import render
from django.http import HttpResponse
from .forms import crawlInitForm
import json

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World!")

def index(request):
    form=crawlInitForm(request.POST)
    return render(request,'index.html',{'crawlForm':form})

def showtime(request):
    # form=crawlInitForm(request.POST)
    return render(request,'showtime.html')

def crawlSite(request):

    # hostSeeds=request.POST['hostSeeds']
    # threadNumber=request.POST['threadNumber']
    list={}
    list['nodes']=[{'name':'hoho','group':1},{'name':'haha','group':2}]
    list['links']=[{"source":1,"target":0,"value":1}]
    # return render(request, 'showtime.html', {'hostSeeds': hostSeeds,'threadNumber':threadNumber})
    return HttpResponse(json.dumps(list), content_type="application/json")