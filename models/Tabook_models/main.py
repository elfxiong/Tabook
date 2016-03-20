import json

from .forms import CustomerCreationForm, RestaurantCreationForm, ReviewCreationForm, ReservationCreationForm
from django.http import JsonResponse
from django.contrib.auth import hashers

from .models import *


# customer
# TODO: override save functions in model class so that we can save in encoded pwd instead of plain text (done)
# TODO: updat function: password need to be encoded

def create_customer(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        print(request.POST)
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # save the fields to a user object but not save to the database
            print("form saved")
            user.save()  # save to the database with hashed password
            print("after save")
            content['success'] = True
            # content['id'] = user.id
            content['user'] = {'id': user.id, 'type': Authenticator.CUSTOMER}
        else:
            content['result'] = "Failed to create a new customer"
            content['html'] = form.errors
    print("content:" + str(content))
    return JsonResponse(content)


def get_customer(request, id):
    content = {"success": False}
    if request.method != 'GET':
        content['result'] = "Invalid request method. Expected GET."
    else:
        try:
            user = Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            content["result"] = "Customer not found"
        else:
            result = {}
            for field_name in ['id', 'username', 'email', 'phone']:
                result[field_name] = getattr(user, field_name)
            content['result'] = result
            content["success"] = True
    return JsonResponse(content)


def update_customer(request):
    content = {'success': False}
    if request.method != "POST":
        content['result'] = "Invalid request method. Expected POST."
    elif 'id' not in request.POST:
        content['result'] = "Customer id not provided"
    else:
        try:
            uid = request.POST['id']
            user = Customer.objects.get(pk=uid)
        except Customer.DoesNotExist:
            content['result'] = "Customer not found"
        else:
            changed = []
            for field_name in ['username', 'password', 'first_name', 'last_name', 'email', 'phone']:
                if field_name in request.POST:
                    value = request.POST[field_name]
                    setattr(user, field_name, value)
                    changed.append(field_name)
            user.save()
            content['changed'] = changed
            content['success'] = True
    return JsonResponse(content)


# restaurant


def create_restaurant(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        print(request.POST)
        form = RestaurantCreationForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.save()
            print("restaurant saved")
            content['success'] = True
            # content['id'] = restaurant.id
            content['user'] = {'id': restaurant.id, 'type': Authenticator.RESTAURANT}
        else:
            content['result'] = "Failed to create a new restaurant"
            content['html'] = form.errors
    print(content, '  test content')
    return JsonResponse(content)


def get_restaurant(request, id):
    content = {"success": False}
    if request.method != 'GET':
        content['result'] = "Invalid request method. Expected GET."
    else:
        try:
            user = Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            content["result"] = "restaurant not found"
        else:
            result = {}
            for field_name in ['id', 'username', 'email', 'phone']:
                result[field_name] = getattr(user, field_name)
            content[result] = result
            content["success"] = True
    return JsonResponse(content)


def update_restaurant(request):
    content = {'success': False}
    if request.method != "POST":
        content['result'] = "Invalid request method. Expected POST."
    elif 'id' not in request.POST:
        content['result'] = "Restaurant id not provided"
    else:
        try:
            uid = request.POST['id']
            user = Restaurant.objects.get(pk=uid)
        except Restaurant.DoesNotExist:
            content['result'] = "Restaurant not found"
        else:
            changed = []
            for field_name in ['username', 'password', 'email', 'phone', 'address', 'price', 'category']:
                if field_name in request.POST:
                    value = request.POST[field_name]
                    setattr(user, field_name, value)
                    changed.append(field_name)
            user.save()
            content['changed'] = changed
            content['success'] = True
    return JsonResponse(content)


# filter restaurants and return a list of restaurants with info
def filter_restaurant(request):
    content = {'success': False}
    if request.method != 'GET':
        content['result'] = "Invalid request method. Expected GET."
    else:
        parameters = ['id', 'username', 'email', 'phone']
        query_attrs = {param: value for param, value in request.GET.items() if param in parameters}
        restaurants = Restaurant.objects.filter(**query_attrs)
        content['success'] = True
        info = ['id', 'username', 'email', 'phone', 'address', 'restaurant_name']
        content['result'] = [{field: getattr(r, field) for field in info} for r in restaurants]
    return JsonResponse(content)


def filter_tables(request):
    content = {'success': False}
    if request.method != 'GET':
        content['result'] = "Invalid request method. Expected GET."
    else:
        parameters = ['id', 'restaurant_id']
        query_attrs = {param: value for param, value in request.GET.items() if param in parameters}
        restaurants = Table.objects.filter(**query_attrs)
        content['success'] = True
        info = ['id', 'restaurant_id', 'capacity', 'style', 'x_coordinate', 'y_coordinate']
        content['result'] = [{field: getattr(r, field) for field in info} for r in restaurants]
    return JsonResponse(content)


def create_review(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        form = ReviewCreationForm({'restaurant': request.POST['restaurant_id'],
                                   'customer': request.POST['customer_id'],
                                   'stars': request.POST['stars'],
                                   'text': request.POST['text']})
        if form.is_valid():
            review = form.save()
            content['success'] = True
            content['id'] = review.id
        else:
            content['result'] = "Failed to create a new review"
            content['html'] = form.errors
    return JsonResponse(content)


def get_reviews(request):
    content = {'success': False}
    if request.method != 'GET':
        content['result'] = "Invalid request method"
    else:
        query_attrs = {'id': request.GET['restaurant_id']}
        restaurant = Restaurant.objects.get(**query_attrs)
        reviews = Review.objects.filter(restaurant=restaurant)
        if reviews:
            infos = ['id', 'stars', 'text', 'created']
            for r in reviews:
                fields = {field: getattr(r, field) for field in infos}
                fields['customer_id'] = r.customer.id  # TODO: fixNote: returns id, not customer data
                content['result'] = [fields]
            content['success'] = True
        else:
            content['result'] = "No reviews found."
    return JsonResponse(content)


# check if the authenticator is valid, and return the user type (customer, restaurant, or anonymous)
def check_authenticator(request):
    content = {'success': False}
    if request.method != 'GET':
        content['result'] = "Invalid request method. Expected GET."
    else:
        content['success'] = True
        token = request.GET['authenticator']
        authenticator = Authenticator.objects.filter(token=token).first()
        if authenticator:
            user_id = authenticator.user_id
            user_type = authenticator.user_type
            if user_type == Authenticator.CUSTOMER:
                user = Customer.objects.get(id=user_id)
            else:
                user = Restaurant.objects.get(id=user_id)
            content['user'] = {'type': user_type, 'id': user_id, 'username': user.username}
        else:
            content['user'] = {'type': 'anonymous'}
    return JsonResponse(content)


# request passes in user information, including type and user_id
def create_authenticator(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = 'Invalid request method. Expected POST.'
    else:
        print('test')
        print(request.POST)
        user = json.loads(request.POST['user'])
        if user['type'] == Authenticator.CUSTOMER:
            authenticator = Authenticator.objects.create(user_id=user['id'],
                                                         user_type=Authenticator.CUSTOMER)
            content['success'] = True
            content['auth'] = authenticator.token
            return JsonResponse(content)

        elif user['type'] == Authenticator.RESTAURANT:
            authenticator = Authenticator.objects.create(user_id=user['id'],
                                                         user_type=Authenticator.RESTAURANT)
            content['success'] = True
            content['auth'] = authenticator.token
            return JsonResponse(content)
        else:
            content['result'] = 'Invalid user type.'
    return JsonResponse(content)


# ???should this use GET or POST
def authenticate_user(request):
    content = {'success': False}
    # check user name and password
    if request.method != 'GET':
        content['result'] = "Invalid request method. Expected GET."
    else:
        username = request.GET['username']
        password = request.GET['password']

        cus = Customer.objects.filter(username=username).first()
        if cus:
            if hashers.check_password(password, cus.password):
                content['success'] = True
                content['result'] = 'Customer authenticated successfully.'
                content['user'] = {'id': cus.id, 'type': Authenticator.CUSTOMER}
            else:
                content['result'] = 'Password does not matched.'
        else:
            res = Restaurant.objects.filter(username=username).first()
            if res:
                if hashers.check_password(password, res.password):
                    content['success'] = True
                    content['result'] = 'Restaurant authenticated successfully.'
                    content['user'] = {'id': res.id, 'type': Authenticator.RESTAURANT}
                else:
                    content['result'] = 'Password does not matched.'
            else:
                content['result'] = "Invalid username name or password."
        return JsonResponse(content)


'''
def login(request):
    content = {'success': False}
    # check user name and password
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        username = request.POST['username']
        password = request.POST['password']
        cus = Customer.objects.filter(username=username, password=password).first()
        if cus:
            authenticator = Authenticator.objects.create(user_id=cus.id, user_type=Authenticator.CUSTOMER)
            content['success'] = True
            content['auth'] = authenticator.token
            return JsonResponse(content)
        else:
            res = Restaurant.objects.filter(username=username, password=password).first()
            if res:
                authenticator = Authenticator.objects.create(user_id=res.id,
                                                             user_type=Authenticator.RESTAURANT)
                content['success'] = True
                content['auth'] = authenticator.token
                return JsonResponse(content)
        content['result'] = "Invalid username name or password."
    return JsonResponse(content)
'''


def create_reservation(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        form = ReservationCreationForm(request.POST)
        if form.is_valid():
            res = form.save()
            content['success'] = True
            content['reservation'] = {'id': res.id}
        else:
            content['result'] = "Failed to create a new reservation."
            content['html'] = form.errors
    return JsonResponse(content)


def get_reservation(request, id):
    content = {"success": False}
    if request.method != 'GET':
        content['result'] = "Invalid request method. Expected GET."
    else:
        try:
            user = Reservation.objects.get(pk=id)
        except Reservation.DoesNotExist:
            content["result"] = "Reservation not found."
        else:
            result = {}
            for field_name in ['id', 'customer', 'status', 'created', 'start_time', 'duration']:
                result[field_name] = getattr(user, field_name)
            content['result'] = result
            content["success"] = True
    return JsonResponse(content)


def update_reservation(request):
    content = {'success': False}
    if request.method != "POST":
        content['result'] = "Invalid request method. Expected POST."
    elif 'id' not in request.POST:
        content['result'] = "Reservation id not provided."
    else:
        try:
            uid = request.POST['id']
            user = Reservation.objects.get(pk=uid)
        except Reservation.DoesNotExist:
            content['result'] = "Reservation not found."
        else:
            changed = []
            for field_name in ['customer', 'status', 'created', 'start_time', 'duration']:
                if field_name in request.POST:
                    value = request.POST[field_name]
                    setattr(user, field_name, value)
                    changed.append(field_name)
            user.save()
            content['changed'] = changed
            content['success'] = True
    return JsonResponse(content)
