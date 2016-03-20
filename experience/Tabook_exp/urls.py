"""Tabook_exp URL Configuration

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
    url(r'^auth/login/$', login),
    url(r'^restaurants/all/$', search_restaurant),
    url(r'^restaurants/(?P<id>\d+)/$', get_restaurant),
    url(r'^restaurants/create/$', create_restaurant),
    url(r'^restaurants/table_status/$', get_table_status),
    url(r'^restaurants/recommendation/$', get_recommendations),
    url(r'^restaurants/$', get_restaurant),
    url(r'^restaurants/featured/$', get_featured),
    url(r'^customers/create_customer/$', create_customer),
    url(r'^customers/get_customer/(?P<id>\d+)/$', get_customer),
    url(r'^tables_by_restaurant_id/(?P<id>\d+)/$', get_tables_by_restaurant_id),

]
