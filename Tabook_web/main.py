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


def restaurant_page(request, id):
    context = {}
    restaurant_id = id
    url = settings.EXP_LAYER_URL + "restaurants/"
    data = requests.get(url, params={'id': restaurant_id})
    restaurant = data.json()['result'][0]
    print(restaurant)
    context['restaurant'] = restaurant
    return render(request, 'left-sidebar.html', context)
