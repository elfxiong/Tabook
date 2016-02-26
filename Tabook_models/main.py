from Tabook_models.forms import CustomerCreationForm, RestaurantCreationForm
from django.http import JsonResponse
from .models import *


# customer


def create_customer(request):
    content = {'success': False}
    if request.method != 'POST':
        content['result'] = "Invalid request method"
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
        content['result'] = "Invalid request method"
    else:
        try:
            user = Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            content["result"] = "Customer not found"
        else:
            for field_name in ['id', 'username', 'email', 'phone']:
                content[field_name] = getattr(user, field_name)
            content["success"] = True
    return JsonResponse(content)


def update_customer(request):
    content = {'success': False}
    if request.method != "POST":
        content['result'] = "Invalid request method"
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
            for field_name in ['username', 'password', 'first_name', 'last_name','email', 'phone']:
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
        content['result'] = "Invalid request method"
    else:
        form = RestaurantCreationForm(request.POST)
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
        content['result'] = "Invalid request method"
    else:
        try:
            user = Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            content["result"] = "restaurant not found"
        else:
            for field_name in ['id', 'username', 'email', 'phone']:
                content[field_name] = getattr(user, field_name)
            content["success"] = True
    return JsonResponse(content)


def update_restaurant(request):
    content = {'success': False}
    if request.method != "POST":
        content['result'] = "Invalid request method"
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


def filter_restaurant(request):
    content = {'success': False}
    if request.method != 'GET':
        content['result'] = "Invalid request method"
    else:
        parameters = ['id', 'username', 'email', 'phone']
        query_attrs = {param: value for param, value in request.GET.items() if param in parameters}
        restaurants = Restaurant.objects.filter(**query_attrs)
        content['success'] = True
        content['result'] = [{'id': r.id, 'username': r.username} for r in restaurants]
    return JsonResponse(content)


#given a table and a date, return the availability of that table at that date time
def table_status(request):
    content = {'success': False}
    if request.method != 'GET':
        content['result'] = "Invalid request method"
    else:
        query_attrs = {'table_id' : request.GET['table_id'], 'date' : request.GET['date']}
        status = TableStatus.objects.filter(**query_attrs)
        if status:
            content['result'] = {'table_status': status[0].available}
            content['success'] = True
    return JsonResponse(content)