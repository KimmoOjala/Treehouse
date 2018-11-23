from django.shortcuts import get_object_or_404, render
import random

from .models import Mineral
from django.template.context_processors import request

def random_mineral_f():
    '''Returns random mineral object.'''
    minerals = Mineral.objects.all()
    mineral_total = len(minerals)
    random_mineral_num = random.randrange(0, mineral_total)
    random_mineral = minerals[random_mineral_num]
    return random_mineral 

def mineral_list(request):
    minerals = Mineral.objects.all()
    random_mineral = random_mineral_f()
    return render(request, 'minerals/mineral_list.html', {'minerals': minerals, "random_mineral": random_mineral})

def mineral_detail(request, pk):
    mineral = get_object_or_404(Mineral, pk=pk)
    random_mineral = random_mineral_f()
    return render(request, 'minerals/mineral_detail.html', {'mineral': mineral, "random_mineral": random_mineral})

