import json
import urllib.request
import requests
from django.http import JsonResponse, HttpResponse
from django.conf import settings

#TODO: call create_authenticator function when register
def get_restaurant(request):
    url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
    id = request.GET['id']
    r = requests.get(url, params={'id': id})
    return JsonResponse(r.json())


def create_restaurant(request):
    content = {"success": False}
    if request.method != "POST":
        content["result"] = "GET Request Recieved. Expected POST."
    else:
        request_url = settings.MODELS_LAYER_URL + "api/restaurants/create/"
        response = requests.post(request_url, data=request.POST) #POST.dict() or POST?
        #content = json.loads(response.content.decode('utf-8'))
        print(response.content, "test response")
        r = json.loads(response.content.decode('utf-8'))
        if r['success']:
            # Models layer failed
            # error = {}
            # if content['result'] == "Invalid request method. Expected POST.":
            #     error["type"] = "GET Request Recieved. Expected POST."
            #     return JsonResponse(error)
            # if content["result"] == "Failed to create a new restaurant":
            #     error["type"] = "Restaurant creation failed."
            # return JsonResponse(error)
            #new customer created
            url = settings.MODELS_LAYER_URL + "api/auth/authenticator/create/"
            data = json.dumps(r['user'])
            r = requests.post(url, data={'user':data}).json()
            if r['success']:
                content['success'] = True
                content['auth'] = r['auth']
            else:
                content['result'] = 'Models layer failed: ' + r['result']
            #content['result'] = "Models layer failed: " + content['result']
        else:
            content['result'] = "Models layer failed: " + r['result']

    return JsonResponse(content)

def create_customer(request):
    content = {"success": False}
    if not request.method == "POST":
        content["result"] = "GET request received. Expected POST."
    else:
        request_url = settings.MODELS_LAYER_URL + "api/customers/create/"
        response = requests.post(request_url, data=request.POST)
        print(response)
        r = response.json() #decode json object response

        #content = json.loads(response.content.decode('utf-8'))
        if r['success']:
            #new customer created
            url = settings.MODELS_LAYER_URL + "api/auth/authenticator/create/"
            data = json.dumps(r['user'])
            print(data)
            r = requests.post(url, data={'user':data}).json()
            if r['success']:
                content['success'] = True
                content['auth'] = r['auth']
            else:
                content['result'] = 'Models layer failed: ' + r['result']

        else:
            #Models layer failed
            content['result'] = "Models layer failed: " + r['result']

    return JsonResponse(content)

def get_customer(request, id):
    content = {"success": False}
    if request.method != 'GET':
        content['result'] = "Invalid request method"
    else:
        request_url = settings.MODELS_LAYER_URL + "api/customers/" + id + "/"
        r = requests.get(request_url)
        r_dict = r.json()
        if not r_dict['success']:
            content['result'] = "Error from the model layer."
        else:
            content["success"] = True
            content["result"] = r_dict["result"]

    return JsonResponse(content)


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


# get featured restaurants with highest rating, for now it shows all restaurants
def get_featured(request):
    url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
    r = requests.get(url).json()
    rest_list = r['result']
    if len(rest_list) > 2:
        rest_list = rest_list[:2]
        r['result'] = rest_list
    return JsonResponse(r)


# get all tables by restaurant
def get_tables_by_restaurant_id(request, id):
    url = settings.MODELS_LAYER_URL + "api/tables/filter/"
    r = requests.get(url, params={'restaurant_id': id}).json()
    return JsonResponse(r)


# get tables by restaurant, date
def filter_table(request):
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

#login: call authenticate_user(GET) and create authenticator(POST) functions
def login(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        url = settings.MODELS_LAYER_URL + "api/auth/authenticate_user/"
        data = {'password': request.POST['password'], 'username': request.POST['username']}
        r = requests.get(url, params=data).json()
        #print(r)
        if r['success']:
            #user authenticated
            url = settings.MODELS_LAYER_URL + "authenticator/create/"
            data = r['user']
            r = requests.post(url, data=data).json()
            if r['success']:
                content['success'] = True
                content['auth'] = r['auth']
            else:
                content['result'] = 'Models layer failed: ' + r['result']
        else:
            content['result'] = 'Models layer failed: '+r['result']
    return JsonResponse(content)


# a helper method that checks the authenticator and gets user type (anonymous/customer/restaurant)
# will be used by views that render different content for different types of user
def get_user_type(token):
    url = settings.MODELS_LAYER_URL + "api/auth/authenticator/check/"
    params = {'authenticator': token}
    r = requests.get(url, params).json()
    if r['success']:
        return r['user']['type']
    else:
        # this method is incorrect or the API has changed
        raise Warning
        # return None
