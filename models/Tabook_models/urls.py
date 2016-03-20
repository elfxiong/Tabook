"""Tabook_models URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from .main import *
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^auth/login/$', login),
    url(r'^api/auth/authenticate_user/$', authenticate_user),
    url(r'^api/auth/authenticator/create/$', create_authenticator),
    url(r'^api/auth/authenticator/check/$', check_authenticator),
    url(r'^api/customers/create/$', create_customer),
    url(r'^api/customers/(?P<id>\d+)/$', get_customer),
    url(r'^api/customers/update/$', update_customer),
    url(r'^api/restaurants/create/$', create_restaurant),
    url(r'^api/restaurants/(?P<id>\d+)/$', get_restaurant),
    url(r'^api/restaurants/update/$', update_restaurant),
    url(r'^api/restaurants/filter/$', filter_restaurant),
    url(r'^api/restaurants/reviews/$', get_reviews),
    url(r'^api/restaurants/reviews/create/$', create_review),
    url(r'^api/tables/filter/$', filter_tables),


]
