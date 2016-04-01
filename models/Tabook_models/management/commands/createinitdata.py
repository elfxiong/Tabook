from django.core.management.base import BaseCommand, CommandError

from Tabook_models.models import *


class Command(BaseCommand):
    help = 'create init data'

    def handle(self, *args, **options):
        Customer.objects.create(username="qx2dk", password="roar", email="roar@lion.zoo", phone="55555")
        Customer.objects.create(username="yn9sa", password="meow", email="meow@cat.zoo", phone="333")
        Customer.objects.create(username="jef6mt", password="pass", email="user@user.com", phone="00000")
        Customer.objects.create(username="user", password="pass", email="user@user.com", phone="00000")
        Customer.objects.create(username="admin", password="admin", email="user@user.com", phone="00000")

        r1 = Restaurant.objects.create(username="lion",
                                       password="roar",
                                       email="roar@lion.zoo",
                                       phone="55555",
                                       restaurant_name="Aha Restaurant",
                                       address="Rice 340",
                                       price_range="2",
                                       category="Pizza")
        r2 = Restaurant.objects.create(username="cat",
                                       password="meow",
                                       email="meow@cat.zoo",
                                       phone="333",
                                       restaurant_name="Blah Cafe",
                                       address="somewhere",
                                       price_range="1",
                                       category="animals")
        r3 = Restaurant.objects.create(username="starbucks",
                                       password="coffee",
                                       email="star@bucks.com",
                                       phone="333",
                                       restaurant_name="Starbucks",
                                       address="123 St",
                                       price_range="5",
                                       category="Coffe")
        r4 = Restaurant.objects.create(username="McDonalds",
                                       password="McDonalds",
                                       email="McDonalds@McDonalds.com",
                                       phone="333",
                                       restaurant_name="McDonalds",
                                       address="124 St",
                                       price_range="1",
                                       category="Fast Food")
        r5 = Restaurant.objects.create(username="Ten",
                                       password="Ten",
                                       email="Ten@Ten.com",
                                       phone="333",
                                       restaurant_name="Ten",
                                       address="126 St",
                                       price_range="5",
                                       category="Sushi")
        r6 = Restaurant.objects.create(username="citizenburger",
                                       password="citizenburger",
                                       email="citizenburger@citizenburger.com",
                                       phone="333",
                                       restaurant_name="Citizen Burger",
                                       address="Main St",
                                       price_range="3",
                                       category="Burgers")
        r7 = Restaurant.objects.create(username="Dominos",
                                       password="Dominos",
                                       email="Dominos@Dominos.com",
                                       phone="333",
                                       restaurant_name="Dominos",
                                       address="123 St",
                                       price_range="2",
                                       category="Pizza")


        Table.objects.create(restaurant=r1, capacity=4)
        Table.objects.create(restaurant=r1, capacity=4)
        Table.objects.create(restaurant=r1, capacity=3)
        Table.objects.create(restaurant=r1, capacity=3)
        Table.objects.create(restaurant=r1, capacity=3)

        Table.objects.create(restaurant=r2, capacity=3)
        Table.objects.create(restaurant=r2, capacity=4)
        Table.objects.create(restaurant=r2, capacity=3)
        Table.objects.create(restaurant=r2, capacity=2)
        Table.objects.create(restaurant=r2, capacity=6)

        Table.objects.create(restaurant=r3, capacity=3)
        Table.objects.create(restaurant=r3, capacity=3)
        Table.objects.create(restaurant=r3, capacity=3)
        Table.objects.create(restaurant=r3, capacity=8)
        Table.objects.create(restaurant=r3, capacity=2)

        Table.objects.create(restaurant=r4, capacity=9)
        Table.objects.create(restaurant=r4, capacity=4)
        Table.objects.create(restaurant=r4, capacity=2)
        Table.objects.create(restaurant=r4, capacity=8)
        Table.objects.create(restaurant=r4, capacity=9)


        Table.objects.create(restaurant=r5, capacity=3)
        Table.objects.create(restaurant=r5, capacity=3)
        Table.objects.create(restaurant=r5, capacity=3)
        Table.objects.create(restaurant=r5, capacity=6)
        Table.objects.create(restaurant=r5, capacity=6)


        Table.objects.create(restaurant=r6, capacity=2)
        Table.objects.create(restaurant=r6, capacity=2)
        Table.objects.create(restaurant=r6, capacity=3)
        Table.objects.create(restaurant=r6, capacity=3)
        Table.objects.create(restaurant=r6, capacity=5)


        Table.objects.create(restaurant=r7, capacity=5)
        Table.objects.create(restaurant=r7, capacity=4)
        Table.objects.create(restaurant=r7, capacity=2)
        Table.objects.create(restaurant=r7, capacity=7)
        Table.objects.create(restaurant=r7, capacity=5)

        self.stdout.write("Done")
