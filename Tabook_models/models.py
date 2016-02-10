from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=20)  # TBD


class Customer(User):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Restaurant(User):
    restaurant_name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    capacity = models.PositiveSmallIntegerField()


class TableStatus(models.Model):  # name TBD
    table = models.ForeignKey(Table)
    date = models.DateTimeField()
    available = models.BooleanField(default=False)


class Reservation:
    customer = models.ForeignKey(Customer)
    table_status = models.ForeignKey(TableStatus)
    status = models.CharField()
    created = models.DateTimeField(auto_created=True, auto_now_add=True)
