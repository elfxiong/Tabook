import json

from django.shortcuts import render


def homepage(request):
    return render(request, 'index.html')


def restaurant_details(request):
    return render(request, 'left-sidebar.html')