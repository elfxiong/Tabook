import json, time,os

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from kafka import KafkaProducer


class Command(BaseCommand):
    help = 'push existing restaurants into kafka'

    def handle(self, *args, **options):
        # time.sleep(10)
        url = settings.MODELS_LAYER_URL + "api/restaurants/filter/"
        try:
            r = requests.get(url).json()
            if r['success']:
                restaurant_list = r['result']
                producer = KafkaProducer(bootstrap_servers='kafka:9092')
                for restaurant in restaurant_list:
                    producer.send('new-restaurant-topic', json.dumps(restaurant).encode('utf-8'))
            else:
                self.stdout('models layer not ready')
                self.handle(*args, **options)
        except Exception as e:
            # TODO retry
            self.stdout(e)
            self.stdout('exception')
            self.handle(*args, **options)
        # pass

        self.stdout.write("Finish")