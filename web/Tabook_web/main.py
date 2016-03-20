import requests
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm


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


# same login for both customer and restaurant
AUTH_COOKIE_KEY = "authenticator"


# TODO hash password somewhere
def login_page(request):
    context = {}
    if request.method == 'GET':
        # next = request.GET.get('next') or reverse('homepage')
        return render(request, 'login.html')
    f = LoginForm(request.POST)
    if not f.is_valid():
        # bogus form post, send them back to login page and show them an error
        print('error', f.errors)
        return render(request, 'login.html')
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    next = f.cleaned_data.get('next') or reverse('homepage')

    url = settings.EXP_LAYER_URL + "auth/login/"
    post_data = {'username': username, 'password': password}
    r = requests.post(url, post_data).json()
    if not r or not r['success']:
        context['message'] = r['result']  # invalid username/password
        return render(request, 'login.html', context)
    response = HttpResponseRedirect(next)
    response.set_signed_cookie(key=AUTH_COOKIE_KEY, value=r['auth'])
    context['result'] = "Successfully logged in. Redirecting."
    return response


# probably need something special for restaurant registration
def signup_page(request):
    return render(request,'signup.html')
