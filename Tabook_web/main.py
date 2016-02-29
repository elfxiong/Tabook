import requests
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    context = {}
    # get recommended url
    url = settings.EXP_LAYER_URL + "restaurants/recommendation/"
    data = requests.get(url)
    # print(data.json())
    context['recommended_restaurants'] = data.json()['result']

    # get featured restaurant
    url = settings.EXP_LAYER_URL + "restaurants/featured/"
    data = requests.get(url).json()
    context['featured_restaurants'] = data['result']


    return render(request, 'index.html', context=context)




def restaurant_page(request, id):
    context = {}
    restaurant_id = id

    # get restaurant info
    url = settings.EXP_LAYER_URL + "restaurants/"
    data = requests.get(url, params={'id': restaurant_id})
    restaurant = data.json()['result'][0]
    # print(restaurant)
    context['restaurant'] = restaurant

    # get restaurant tables
    url = settings.EXP_LAYER_URL + "tables_by_restaurant_id/" + restaurant_id + "/"
    data = requests.get(url).json()
    if not data['success']:
        pass
    else:
        tables = data['result']
        context['tables'] = tables
    return render(request, 'restaurant.html', context)


def restaurant_list(request):
    context = {}
    url = settings.EXP_LAYER_URL + "restaurants/all/"
    data = requests.get(url).json()
    # print(data.json())
    context['restaurants'] = data['result']
    return render(request, 'restaurants.html', context)
