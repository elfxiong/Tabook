from django.contrib import admin
from .models import User, Customer, Restaurant, Table, TableStatus, Reservation


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass
