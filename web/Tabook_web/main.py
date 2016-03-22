import json

import requests
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, SignUpForm, ReservationForm


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

    context['username'] = get_user_info(request)
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

    authenticator = request.COOKIES.get(AUTH_COOKIE_KEY, "")
    if authenticator:
        f = ReservationForm(request.POST)
        context['form'] = f
        if request.method == "POST" and f.is_valid():
            url = settings.EXP_LAYER_URL + "customers/create_reservation/"
            reservation_details = {'table': f.clened_data['table'], 'start_time': f.cleaned_data['start_time'],
                                   'end_time': f.cleaned_data['end_time']}
            data = {'authenticator': authenticator, 'reservation_details': json.dumps(reservation_details)}
            r = requests.post(url, data).json()
            print(r)
            pass
            # TODO
        else:
            pass

    context['username'] = get_user_info(request)
    return render(request, 'restaurant.html', context)


def restaurant_list(request):
    context = {}
    url = settings.EXP_LAYER_URL + "restaurants/all/"
    data = requests.get(url).json()
    # print(data.json())
    context['restaurants'] = data['result']

    context['username'] = get_user_info(request)
    return render(request, 'restaurants.html', context)


# same login for both customer and restaurant
AUTH_COOKIE_KEY = "authenticator"


def login_page(request):
    context = {}
    context['username'] = get_user_info(request)
    if request.method == 'GET':
        return render(request, 'login.html')
    f = LoginForm(request.POST)
    context['form'] = f
    if not f.is_valid():
        # bogus form post, send them back to login page and show them an error
        print('error', f.errors)
        return render(request, 'login.html', context)
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']

    # TODO: make next functional
    next = f.cleaned_data.get('next') or reverse('homepage')

    url = settings.EXP_LAYER_URL + "auth/login/"
    post_data = {'username': username, 'password': password}
    r = requests.post(url, post_data).json()
    if not r or not r['success']:
        context['message'] = r['result']  # invalid username/password
        return render(request, 'login.html', context)
    response = HttpResponseRedirect(next)
    response.set_cookie(key=AUTH_COOKIE_KEY, value=r['auth'])
    context['result'] = "Successfully logged in. Redirecting."
    return response


# probably need something special for restaurant registration
def signup_page(request):
    context = {}
    context['username'] = get_user_info(request)

    if request.method == 'GET':
        print("signup_page get request recieved")
        return render(request, 'signup.html')

    f = SignUpForm(request.POST)
    context['form'] = f
    if not f.is_valid():
        print("signup_page invalid form")
        # bogus form post, send them back to login page and show them an error
        print('error', f.errors)
        return render(request, 'signup.html', context)
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']

    # TODO: make next functional
    next = f.cleaned_data.get('next') or reverse('homepage')

    url = settings.EXP_LAYER_URL + "customers/create_customer/"
    post_data = {'username': username, 'password': password}
    print("postdata,", post_data)
    r = requests.post(url, post_data).json()
    if not r or not r['success']:
        print("signup_page experience layer not successful")
        context['message'] = r['result']  # invalid username/password
        return render(request, 'signup.html', context)
    response = HttpResponseRedirect(next)
    response.set_cookie(key=AUTH_COOKIE_KEY, value=r['auth'])
    context['result'] = "Successfully logged in. Redirecting."
    print("singup_page returned successfully, returning")
    return response


# helper method that takes in a request and use the cookie to figure out the type of user
def get_user_info(request):
    authenticator = request.COOKIES.get(AUTH_COOKIE_KEY, "")
    if not authenticator:
        return "No auth Anonymous"

    url = settings.EXP_LAYER_URL + "auth/user/"
    params = {"authenticator": authenticator}
    print(requests.get(url, params))
    r = requests.get(url, params).json()
    if r['success']:
        return r['user']
    else:
        return "Not Success Anonymous"


def logout(request):
    authenticator = request.COOKIES.get(AUTH_COOKIE_KEY, "")
    if not authenticator:
        return HttpResponseRedirect(reverse('login_page'))
    url = settings.EXP_LAYER_URL + "auth/logout/"
    data = {"authenticator": authenticator}
    r = requests.post(url, data=data)
    #if not r['success']:

    response = HttpResponseRedirect(reverse("homepage"))
    response.delete_cookie(AUTH_COOKIE_KEY)
    return response


def reservation_history(request):
    context = {}
    authenticator = request.COOKIES.get(AUTH_COOKIE_KEY, "")
    if not authenticator:
        return HttpResponseRedirect(reverse('login_page'))

    url = settings.EXP_LAYER_URL + "customers/reservation_history/"
    params = {"authenticator": authenticator}
    r = requests.get(url, params).json()
    if not r['success']:
        return HttpResponse(r['result'])
    context['reservations'] = r['result']
    context['username'] = get_user_info(request)
    return render(request, 'reservation-history.html', context)

# def create_reservation(request):
#     context = {}
#     authenticator = request.COOKIES.get(AUTH_COOKIE_KEY, "")
#     if not authenticator:
#         return HttpResponseRedirect(reverse('login_page'))
#
#     if request.method != 'POST':
#         return HttpResponse("Invalid request method")
#
#     f = ReservationForm(request.POST)
#     context['form'] = f
#     if f.is_valid():
#         url = settings.EXP_LAYER_URL + "customers/create_reservation/"
#         reservation_details = {'table': f.clened_data['table'], 'start_time': f.cleaned_data['start_time'],
#                                'end_time': f.cleaned_data['end_time']}
#         data = {'authenticator': authenticator, 'reservation_details': json.dumps(reservation_details)}
#         r = requests.post(url, data).json()
#         print(r)
#         pass
#         # TODO
#     else:
#         pass
#     return render(request, 'create_reservation.html', context)
