from django.db import models
from datetime import datetime


class Authenticator(models.Model):
    type_choices = (('C', 'Customer'), ('R', 'Restaurant'))
    user_type = models.CharField(max_length=2, choices = type_choices, default='C')
    user_id = models.PositiveIntegerField()
    authenticator = models.CharField()
    date_created = models.DateTimeField(auto_created=True, auto_now_add=True)

    
class User(models.Model):
    username = models.CharField(max_length=40)  # need setter
    password = models.CharField(max_length=128)  # need setter
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)  # need setter

    def __str__(self):
        return str(self.id) + " " + self.username

    class Meta:
        abstract = True


class Customer(User):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)


class Restaurant(User):
    restaurant_name = models.CharField(max_length=30) # Should this be unique(??)
    address = models.CharField(max_length=200)
    price_range = models.PositiveSmallIntegerField(default=0)  # number of dollar signs
    category = models.CharField(max_length=30, default="unclassified")


class RestaurantHours(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    monday_open_time = models.TimeField(default='0:00')
    monday_close_time = models.TimeField(default='23:59')
    tuesday_open_time = models.TimeField(default='0:00')
    tuesday_close_time = models.TimeField(default='23:59')
    wednesday_open_time = models.TimeField(default='0:00')
    wednesday_close_time = models.TimeField(default='23:59')
    thursday_open_time = models.TimeField(default='0:00')
    thursday_close_time = models.TimeField(default='23:59')
    friday_open_time = models.TimeField(default='0:00')
    friday_close_time = models.TimeField(default='23:59')
    saturday_open_time = models.TimeField(default='0:00')
    saturday_close_time = models.TimeField(default='23:59')
    sunday_open_time = models.TimeField(default='0:00')
    sunday_close_time = models.TimeField(default='23:59')

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    capacity = models.PositiveSmallIntegerField()
    style = models.CharField(max_length=30, default='unspecified')
    x_coordinate = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # XXXXX.XX
    y_coordinate = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # XXXXX.XX


class Reservation(models.Model):
    customer = models.ForeignKey(Customer)
    status = models.CharField(max_length=30) # possible values ???
    created = models.DateTimeField(auto_created=True, auto_now_add=True)
    start_time = models.DateTimeField(default=datetime.now, blank=True)
    duration = models.PositiveSmallIntegerField(default=1)  # number of minutes

class Review(models.Model):
    customer = models.ForeignKey(Customer)
    restaurant = models.ForeignKey(Restaurant)
    stars = models.PositiveSmallIntegerField(default=0) # number of stars 0-5
    text = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_created=True, auto_now_add=True)


