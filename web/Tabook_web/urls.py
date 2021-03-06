"""Tabook_web URL Configuration

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
from Tabook_web.main import *
from django.conf.urls import url
from django.contrib import admin
from . import main

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main.homepage, name='homepage'),
    url(r'^restaurants/(?P<id>\d+)/', main.restaurant_page, name='restaurant_page'),
    url(r'^restaurants/', main.restaurant_search, name='restaurant_list'),
    url(r'^login/', main.login_page, name='login_page'),
    url(r'^signup/', main.signup_page, name='signup_page'),
    url(r'^logout/', main.logout, name='logout'),
    url(r'^reservation/history', main.reservation_history, name='reservation_history'),
    url(r'^reservation/search', main.reservation_search, name='reservation_search'),
]
