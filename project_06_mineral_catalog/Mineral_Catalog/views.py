from django.shortcuts import render
from django.template.context_processors import request


def index(request):
    return render(request, 'index.html')

