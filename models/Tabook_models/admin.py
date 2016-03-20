from django.contrib import admin
from .models import User, Customer, Restaurant, Table, Reservation, Authenticator


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(Table)
class RestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class RestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(Authenticator)
class Authenticator(admin.ModelAdmin):
    pass
