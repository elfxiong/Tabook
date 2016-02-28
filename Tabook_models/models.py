from django.db import models


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
    hours = models.ForeignKey(RestaurantHours)
    price_range = models.PositiveSmallIntegerField(default=0)  # number of dollar signs
    category = models.CharField(max_length=30, default="unclassified")


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
    start_time = models.DateTimeField()
    duration = models.TimeField()


class RestaurantHours(models.Model):
    monday_open_time = models.TimeField()
    monday_close_time = models.TimeField()
    tuesday_open_time = models.TimeField()
    tuesday_close_time = models.TimeField()
    wednesday_open_time = models.TimeField()
    wednesday_close_time = models.TimeField()
    thursday_open_time = models.TimeField()
    thursday_close_time = models.TimeField()
    friday_open_time = models.TimeField()
    friday_close_time = models.TimeField()
    saturday_open_time = models.TimeField()
    saturday_close_time = models.TimeField()
    sunday_open_time = models.TimeField()
    sunday_close_time = models.TimeField()


class Review(models.Model):
    customer = models.ForeignKey(Customer)
    restaurant = models.ForeignKey(Restaurant)
    stars = models.PositiveSmallIntegerField(default=0) # number of stars 0-5
    text = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_created=True, auto_now_add=True)


