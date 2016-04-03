from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json

consumer = None
es = None

while not consumer or not es:
    try:
        consumer  = KafkaConsumer('new-restaurant-topic', group_id='restaurant-indexer', bootstrap_servers=['kafka:9092'])
        es = Elasticsearch(['es'])
    except:
        print('fail to create restaurant topic')
        pass
print('test')
for message in consumer:
    print("restuanrt for loop")
    new_listing = json.loads((message.value).decode('utf-8'))
    print("")

    # resaurant_id = new_listing['resaurant_id']
    # restaurant_name = new_listing['restaurant_name']
    # address = new_listing['address']
    # price_range = new_listing['price_range']
    # category = new_listing['category']
    #
    # monday_open_time = new_listing['monday_open_time']
    # monday_close_time = new_listing['monday_close_time']
    # tuesday_open_time = new_listing['tuesday_open_time']
    # tuesday_close_time = new_listing['tuesday_close_time']
    # wednesday_open_time = new_listing['wednesday_open_time']
    # wednesday_close_time = new_listing['wednesday_close_time']
    # thursday_open_time = new_listing['thursday_open_time']
    # thursday_close_time = new_listing['thursday_close_time']
    # friday_open_time = new_listing['friday_open_time']
    # friday_close_time = new_listing['friday_close_time']
    # saturday_open_time = new_listing['saturday_open_time']
    # saturday_close_time = new_listing['saturday_close_time']
    # sunday_open_time = new_listing['sunday_open_time']
    # sunday_close_time = new_listing['sunday_close_time']
    #
    # some_new_listing = {
    #     'resaurant_id':resaurant_id,
    #     'restaurant_name':restaurant_name,
    #     'address':address,
    #     'price_range': price_range,
    #     'category':category,
    #     'monday_open_time':monday_open_time,
    #     'monday_close_time':monday_close_time,
    #     'tuesday_open_time':tuesday_open_time,
    #     'tuesday_close_time':tuesday_close_time,
    #     'wednesday_open_time':wednesday_open_time,
    #     'wednesday_close_time':wednesday_close_time,
    #     'thursday_open_time':thursday_open_time,
    #     'thursday_close_time':thursday_close_time,
    #     'friday_open_time':friday_open_time,
    #     'friday_close_time':friday_close_time,
    #     'saturday_open_time':saturday_open_time,
    #     'saturday_close_time':saturday_close_time,
    #     'sunday_open_time':sunday_open_time,
    #     'sunday_close_time':sunday_close_time,
    # }

    es.index(index='restaurant_index', doc_type='listing', id=new_listing['id'], body=new_listing)
    es.indices.refresh(index='restaurant_index')
