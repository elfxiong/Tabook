from django.core.management.base import BaseCommand, CommandError

from Tabook_models.models import *


class Command(BaseCommand):
    help = 'create init data'

    def handle(self, *args, **options):
        Customer.objects.create(username="qx2dk", password="roar", email="roar@lion.zoo", phone="55555")
        Customer.objects.create(username="yn9sa", password="meow", email="meow@cat.zoo", phone="333")
        Customer.objects.create(username="user", password="pass", email="user@user.com", phone="00000")

        r1 = Restaurant.objects.create(username="lion", password="roar", email="roar@lion.zoo", phone="55555",
                                       restaurant_name="Aha Restaurant", address="Rice 340")
        r2 = Restaurant.objects.create(username="cat", password="meow", email="meow@cat.zoo", phone="333",
                                       restaurant_name="Blah Cafe", address="somewhere")

        Table.objects.create(restaurant=r1, capacity=4)
        Table.objects.create(restaurant=r1, capacity=4)
        Table.objects.create(restaurant=r1, capacity=3)
        Table.objects.create(restaurant=r1, capacity=3)
        Table.objects.create(restaurant=r1, capacity=3)

        Table.objects.create(restaurant=r2, capacity=3)
        Table.objects.create(restaurant=r2, capacity=3)
        Table.objects.create(restaurant=r2, capacity=3)
        Table.objects.create(restaurant=r2, capacity=2)
        Table.objects.create(restaurant=r2, capacity=2)

        self.stdout.write("Done")
