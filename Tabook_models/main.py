from Tabook_models.forms import CustomerCreationForm, RestaurantCreationForm, ReviewCreationForm
from django.http import JsonResponse
from .models import *
import urllib
import json


# customer


def create_customer(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method. Expected POST."
    else:
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            content['success'] = True
            content['id'] = user.id
        else:
            content['result'] = "Failed to create a new customer"
            content['html'] = form.errors
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
        form = RestaurantCreationForm(request.POST.dict())
        if form.is_valid():
            restaurant = form.save()
            content['success'] = True
            content['id'] = restaurant.id
        else:
            content['result'] = "Failed to create a new restaurant"
            content['html'] = form.errors
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
                                   'customer'  : request.POST['customer_id'],
                                   'stars'     : request.POST['stars'],
                                   'text'      : request.POST['text']})
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
        query_attrs = {'id' : request.GET['restaurant_id']}
        restaurant = Restaurant.objects.get(**query_attrs)
        reviews = Review.objects.filter(restaurant=restaurant)
        print(reviews)
        if reviews:
            infos = ['id', 'stars', 'text', 'created']
            for r in reviews:
                fields = {field: getattr(r, field) for field in infos}
                fields['customer_id'] = r.customer.id           # TODO: fixNote: returns id, not customer data
                content['result'] = [fields]
            content['success'] = True
        else:
            content['result'] = "No reviews found."
    return JsonResponse(content)
