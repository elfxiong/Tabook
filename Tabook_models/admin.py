from django.contrib import admin
from .models import User, Customer, Restaurant, Table, TableStatus, Reservation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
