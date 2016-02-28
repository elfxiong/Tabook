import requests
from django.conf import settings
from django.shortcuts import render


def homepage(request):
    context = {}
    # get recommended url
    url = settings.EXP_LAYER_URL + "restaurants/recommendation/"
    data = requests.get(url)
    # print(data.json())
    context['recommended_restaurants'] = data.json()['result']
    return render(request, 'index.html', context=context)


def restaurant_details(request):
    return render(request, 'left-sidebar.html')
