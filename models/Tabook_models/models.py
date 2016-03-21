import os

import hmac
from django.conf import settings

from django.db import models
from datetime import datetime
from django.contrib.auth import hashers


class Authenticator(models.Model):
    CUSTOMER = "C"
    RESTAURANT = "R"
    USER_TYPE_CHOICES = ((CUSTOMER, 'Customer'), (RESTAURANT, 'Restaurant'))
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, default='C')
    user_id = models.PositiveIntegerField()
    token = models.CharField(primary_key=True, max_length=64)
    date_created = models.DateTimeField(auto_created=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        while not self.token:
            token = hmac.new(key=settings.SECRET_KEY.encode('utf-8'), msg=os.urandom(32),
                             digestmod='sha256').hexdigest()
            if not Authenticator.objects.filter(pk=token).count():
                self.token = token
        super(Authenticator, self).save(*args, **kwargs)


class User(models.Model):
    username = models.CharField(max_length=40)  # need setter
    password = models.CharField(max_length=128)  # need setter
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)  # need setter

    def __str__(self):
        return str(self.id) + " " + str(self.username)

    class Meta:
        abstract = True


class Customer(User):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    def save(self, *args, **kwargs):
        # salt?
        print("saving")
        hashed_password = hashers.make_password(self.password)
        self.password = hashed_password
        print("saved: " + hashed_password)

        super(Customer, self).save(*args, **kwargs)
        print("saved successfully")


class Restaurant(User):
    restaurant_name = models.CharField(max_length=30, null=True, blank=True)  # Should this be unique(??)
    address = models.CharField(max_length=200, null=True, blank=True)
    price_range = models.PositiveSmallIntegerField(default=0, null=True, blank=True)  # number of dollar signs
    category = models.CharField(max_length=30, default="unclassified", null=True, blank=True)

    def save(self, *args, **kwargs):
        hashed_password = hashers.make_password(self.password)
        self.password = hashed_password
        super(Restaurant, self).save(*args, **kwargs)


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
    status = models.CharField(max_length=30, default="active")  # possible values: active, confirmed, cancelled, pending(?), ????
    created = models.DateTimeField(auto_created=True, auto_now_add=True)
    start_time = models.DateTimeField( auto_now_add=True)  # have better default value?
    end_time = models.DateTimeField(auto_now_add=True)

    @property
    def duration(self):
        return self.end_time - self.start_time  # not tested


class Review(models.Model):
    customer = models.ForeignKey(Customer)
    restaurant = models.ForeignKey(Restaurant)
    stars = models.PositiveSmallIntegerField(default=0)  # number of stars 0-5
    text = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_created=True, auto_now_add=True)
