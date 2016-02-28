import json
import urllib.parse
import urllib.request

from django.http import JsonResponse
from django.conf import settings


def get_restaurant(request, id):
    content = {"success": False}
    if request.method != "GET":
        content["result"] = "POST Request Recieved. Expected GET."
    else:
        id = id
        # Sanitize ID
        request_url = settings.MODELS_LAYER_URL + "api/restaurants/" + id + "/"
        req = urllib.request.Request(request_url, method='GET')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        content = json.loads(resp_json)
        if not content['success']:
            # Models layer failed
            error = {}
            if content['result'] == "Invalid request method":
                error["type"] = "POST Request Recieved. Expected GET."
                return json.loads(error)

            if content["result"] == "Restaurant not found":
                error["type"] = "The requested restaurant was not found."
            return JsonResponse(error)
    return JsonResponse(content)


def create_restaurant(request):
    content = {"success": False}
    if request.method != "POST":
        content["result"] = "GET Request Recieved. Expected POST."
    else:
        request_url = settings.MODELS_LAYER_URL + "api/restaurants/create/"
        print(request.POST)
        req = urllib.request.Request(request_url, method='POST', data=str(request.POST).encode('utf-8')) # data is bytes obj
        req.add_header('Content-Length', len(request.POST))
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        content = json.loads(resp_json)
        print("---------\n",content)
        if not content['success']:
            # Models layer failed
            error = {}
            if content['result'] == "Invalid request method":
                error["type"] = "GET Request Recieved. Expected POST."
                return JsonResponse(error)
            if content["result"] == "restaurant not found":
                error["type"] = "Restaurant creation failed."
            return JsonResponse(error)
    return JsonResponse(content)



def get_customer(request):
    pass




#given a table id and a date, return the availability of that table at that date time
def get_table_status(request):
    request_url = settings.MODELS_LAYER_URL + "api/restaurants/table_request/"
    req = urllib.request.Request(request_url, method='GET')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    table_status = json.loads(resp_json)
    return JsonResponse(table_status)


# search by location, price, category, restaurant name
def search_restaurant(request):
    request_url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
    req = urllib.request.Request(request_url, method='GET')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    restaurants = json.loads(resp_json)
    return JsonResponse(restaurants)


# generate recommendations nearby you
def get_recommendations(request):
    pass


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
