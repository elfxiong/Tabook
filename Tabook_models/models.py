from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)  # need setter
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
    restaurant_name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    price = models.PositiveSmallIntegerField() #number of dollar signs
    category = models.CharField(max_length=30) 


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    capacity = models.PositiveSmallIntegerField()
    shape = models.CharField(max_length=30)
    x_coordinate = models.DecimalField()
    y_coordinate = models.DecimalField()


class TableStatus(models.Model):  # name TBD
    table = models.ForeignKey(Table)
    date = models.DateTimeField()
    available = models.BooleanField(default=False)


class Reservation:
    customer = models.ForeignKey(Customer)
    table_status = models.ForeignKey(TableStatus)
    status = models.CharField()
    created = models.DateTimeField(auto_created=True, auto_now_add=True)
