import json
import urllib.request
import requests
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from kafka import KafkaProducer
from elasticsearch import Elasticsearch


def get_restaurant(request):
    url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
    id = request.GET['id']
    r = requests.get(url, params={'id': id})
    return JsonResponse(r.json())


# TODO This method needs cleanup. Or we just remove it because we don't need it.
def create_restaurant(request):
    content = {"success": False}
    if request.method != "POST":
        content["result"] = "GET Request Received. Expected POST."
    else:
        request_url = settings.MODELS_LAYER_URL + "api/restaurants/create/"
        response = requests.post(request_url, data=request.POST)  # POST.dict() or POST?
        r = json.loads(response.content.decode('utf-8'))
        if r['success']:
            # reservation_info = json.load(content['reservation'])
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            new_listing = request.POST
            new_listing['restaurant_id'] = r['user']['id']
            producer.send('new-restaurant-topic', json.dumps(new_listing).encode('utf-8'))

        if r['success']:
            url = settings.MODELS_LAYER_URL + "api/auth/authenticator/create/"
            data = json.dumps(r['user'])
            r = requests.post(url, data={'user': data, 'username': request.POST['username'],
                                         'password': request.POST['password']}).json()

            if r['success']:
                content['success'] = True
                content['auth'] = r['auth']
            else:
                content['result'] = 'Models layer failed: ' + r['result']
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
        r = response.json()  # decode json object response
        if r['success']:
            # new customer created
            url = settings.MODELS_LAYER_URL + "api/auth/authenticator/create/"
            data = json.dumps(r['user'])
            print(data)
            r = requests.post(url, data={'user': data, 'username': request.POST['username'],
                                         'password': request.POST['password']}).json()
            if r['success']:
                content['success'] = True
                content['auth'] = r['auth']
            else:
                content['result'] = 'Models layer failed: ' + r['result']

        else:
            # Models layer failed
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


def all_restaurants(request):
    url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
    r = requests.get(url).json()
    return JsonResponse(r)


# search by location, price, category, restaurant name
def search_restaurant(request):
    content = {'success': False}
    query = request.GET['query']
    es = Elasticsearch(['es'])
    # es.indices.refresh(index='restaurant_index')
    result = es.search(index='restaurant_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
    content['success'] = True
    content['result'] = [hit['_source'] for hit in result['hits']['hits']]
    return JsonResponse(content)


# generate recommendations nearby you
def get_recommendations(request):
    url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
    r = requests.get(url)
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


# login: call authenticate_user(GET) and create authenticator(POST) functions
def login(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        url = settings.MODELS_LAYER_URL + "api/auth/check_password/"
        data = {'password': request.POST['password'], 'username': request.POST['username']}
        r = requests.get(url, params=data).json()
        if r['success']:
            # user authenticated
            url = settings.MODELS_LAYER_URL + "api/auth/authenticator/create/"
            data = json.dumps(r['user'])
            r = requests.post(url, data={'user': data, 'username': request.POST['username'],
                                         'password': request.POST['password']}).json()
            if r['success']:
                content['success'] = True
                content['auth'] = r['auth']
            else:
                content['result'] = 'Models layer failed: ' + r['result']
        else:
            content['result'] = 'Models layer failed: ' + r['result']
    return JsonResponse(content)


# logout: call delete authenticator function
def logout(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        url = settings.MODELS_LAYER_URL + "api/auth/authenticator/delete/"
        r = requests.post(url, data=request.POST).json()  # {'authenticator':xxxxxxxxx}
        if r['success']:
            content['success'] = True
        else:
            content['result'] = 'Models layer failed: ' + r['result']
    return JsonResponse(content)


# signup: call create_user(GET) and create authenticator(POST) functions
def signup(request):
    pass


# take in authenticator token and check to see if user is authenticated, and if yes then return user info (username)
def authenticate(request):
    content = {'success': False}
    if request.method != 'GET':
        content['result'] = "Invalid request method. Expected GET."
    else:
        content = get_user(request.GET.get('authenticator', ""))
    return JsonResponse(content)


# a helper method that checks the authenticator and gets user info (type:anonymous/customer/restaurant;id;username)
# will be used by views that render different content for different types of user
def get_user(token):
    url = settings.MODELS_LAYER_URL + "api/auth/authenticator/check/"
    params = {'authenticator': token}
    r = requests.get(url, params).json()
    return r  # r = {success: True, user: {type: ###, id: ###, username: ###}}


# same login for both customer and restaurant
AUTH_COOKIE_KEY = "authenticator"


# request.POST holds: user token (authenticator), reservation detials
# needs to send: customerID, start_time, end_time
def create_reservation(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        # AUTHENTICATE USER (get customer ID)
        authenticator = request.POST['authenticator']
        if not authenticator:
            return "No auth Anonymous"
        r = get_user(authenticator)
        if r['success']:
            # call function to put a new listing into model
            url = settings.MODELS_LAYER_URL + "api/reservations/create/"
            dt = json.loads(request.POST['reservation_details'])
            params = dt
            # print(r['user']['id'])
            params['customer'] = r['user']['id']
            content = requests.post(url, params).json()
            if content['success']:
                # add listing into kafka
                reservation_info = content['reservation']
                # reservation_info = json.load(content['reservation'])
                producer = KafkaProducer(bootstrap_servers='kafka:9092')
                new_listing = dt  # containing table, start_time, end_time TODO: need created_time to be returned back here
                new_listing['customer'] = r['user']['id']
                new_listing['created'] = reservation_info['created']  # right?
                new_listing['id'] = reservation_info['id']
                new_listing['restaurant_name'] = reservation_info['restaurant_name']
                producer.send('new-listings-topic', json.dumps(new_listing).encode('utf-8'))

            else:
                # failed to add it to the database
                return JsonResponse(content)
        else:
            content['result'] = "User not authenticated."
    print(content)
    return JsonResponse(content)


def search_reservation(request):
    content = {'success': False}
    if request.method != 'GET':
        content['result'] = "Invalid request method. Expected GET."
    else:
        query = request.GET['query']
        customer_id = request.GET['customer_id']
        es = Elasticsearch(['es'])
        result = es.search(index='listing_index', body={"query" : {
                                                            "filtered" : {
                                                                "filter" : {
                                                                    "match" : {
                                                                        "customer" : customer_id
                                                                    }
                                                                },
                                                                "query" : {
                                                                    "query_string" : {
                                                                        "query" : query
                                                                    }
                                                                }
                                                            }
                                                        }, 'size':10
                                                        })
        content['success'] = True
        content['result'] = [hit['_source'] for hit in result['hits']['hits']]
    return JsonResponse(content)


# take in authenticator and return reservation history
def get_reservation_history(request):
    content = {'success': False}
    if not request.method == "GET":
        content['result'] = "Expecting GET."
    else:
        authenticator = request.GET.get('authenticator', "")
        if not authenticator:
            content['result'] = "User not authenticated. Please pass in authenticator."
        else:
            r = get_user(token=authenticator)
            print('after exp authenticator check: ', r)
            if r['success']:
                if 'user' not in r or 'type' not in r['user']:
                    raise Warning  # API changed?
                elif r['user']['type'] == "Anonymous":
                    content['result'] = "User not authenticated. Please log in."
                elif r['user']['type'] == "C":
                    request_url = settings.MODELS_LAYER_URL + "api/reservations/filter/"
                    # request_url = settings.MODELS_LAYER_URL + "api/reservations/"
                    # resp = requests.get(request_url, data=request.GET).json()
                    params = {'customer': r['user']['id']}
                    resp = requests.get(request_url, params=params).json()
                    print('resp, ', resp)
                    if not resp['success']:
                        content['result'] = "Model layer error: " + str(resp['result'])
                    else:
                        content['result'] = resp['result']
                        content['success'] = True
                elif r['user']['type'] == "R":
                    content['result'] = "Restaurant users do not have a reservation history."
                else:
                    content['result'] = "Unrecognized user type: " + str(r['user']['type'])
            else:
                raise Warning  # wrong request method used?
    return JsonResponse(content)
