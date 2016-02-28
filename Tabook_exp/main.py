import json
from urllib.parse import urlencode
import urllib.request
import requests

from django.http import JsonResponse, HttpResponse
from django.conf import settings


def get_restaurant(request):
    url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
    id = request.GET['id']
    r = requests.get(url, params={'id': id})
    return JsonResponse(r.json())


def get_customer(request):
    pass


# given a table id and a date, return the availability of that table at that date time
def get_table_status(request):
    table_id = request.GET['table_id']
    date = request.GET['date']
    d = {'table_id': table_id, 'date': date}
    request_url = settings.MODELS_LAYER_URL + "api/restaurants/table_status/"
    r = requests.get(request_url, params=d)

    return HttpResponse(r.text)


# search by location, price, category, restaurant name
def search_restaurant(request):
    # request.GET
    request_url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
    req = urllib.request.Request(request_url, method='GET')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    restaurants = json.loads(resp_json)
    return JsonResponse(restaurants)


# generate recommendations nearby you
def get_recommendations(request):
    url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
    r = requests.get(url)
    # print("rec: " + str(r.json()))
    return JsonResponse(r.json())


# get all tables by restaurant, date, time
def get_all_tables(request):
    pass


def get_current_date(request):
    pass


def get_reviews(request):
    pass


# get details (for the mouseover pop-up)
def get_table_details(request):
    pass


# might not need this one for project 3
def get_shopping_cart(request):
    pass


# might not need this one for project 3
# logged in or not; customer or restaurant
def get_user_status(request):
    pass


# might not need this one for project 3
def get_background_image(request):
    pass


# sort the search results by user's pref (distance, price etc), into a specific order
# might not need this one for project 3
def sort_by_preference(request):
    pass
