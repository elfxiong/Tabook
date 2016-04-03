import json, time, os

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from kafka import KafkaProducer
from elasticsearch import Elasticsearch


class Command(BaseCommand):
    help = 'push existing restaurants into kafka'

    def handle(self, *args, **options):
        es = Elasticsearch(['es'])

        # time.sleep(10)
        url = settings.MODELS_LAYER_URL + "api/reservations/filter/"
        try:
            r = requests.get(url).json()
            # self.stdout.write("The reservations in the database:")
            # self.stdout.write(str(r))
            if r['success']:
                reservation_list = r['result']
                # producer = KafkaProducer(bootstrap_servers='kafka:9092')
                for reservation in reservation_list:
                    es.index(index='listing_index', doc_type='listing', id=reservation['id'],
                             body=reservation)
                    # producer.send('new-listings-topic', json.dumps(reservation).encode('utf-8'))
            else:
                self.stdout.write('models layer not ready')
                # self.handle(*args, **options)
        except Exception as e:
            # TODO retry
            self.stdout.write('exception in reservation')
            self.stdout.write(str(e))
            self.handle(*args, **options)

        # pass
        es.indices.refresh(index="listing_index")
        self.stdout.write("Finish Reservations")

        url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
        try:
            r = requests.get(url).json()
            self.stdout.write(str(r))
            if r['success']:
                restaurant_list = r['result']
                # producer = KafkaProducer(bootstrap_servers='kafka:9092')
                for restaurant in restaurant_list:
                    es.index(index='restaurant_index', doc_type='listing', id=restaurant['id'],
                             body=restaurant)
                    # producer.send('new-restaurant-topic', json.dumps(restaurant).encode('utf-8'))
            else:
                self.stdout.write('models layer not ready')
                # self.handle(*args, **options)
        except Exception as e:
            # TODO retry
            self.stdout.write(str(e))
            self.stdout.write('exception')
            self.handle(*args, **options)
        # pass
        es.indices.refresh(index="restaurant_index")
        self.stdout.write("Finish Restaurants")
