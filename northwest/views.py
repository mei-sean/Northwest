from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request handler

def say_hello(request):
    #can do whatever in here like data from db
    return HttpResponse('NORTHWEST UNDER CONSTRUCTION')


