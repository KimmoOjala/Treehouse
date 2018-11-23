from django.shortcuts import render
from django.template.context_processors import request


def hello_world(request):
    return render(request, 'home.html')

