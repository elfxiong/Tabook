from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json

consumer = None
es = None

while not consumer or not es:
    try:
        consumer  = KafkaConsumer('new-restaurant-topic', group_id='restaurant-indexer', bootstrap_servers=['kafka:9092'])
        es = Elasticsearch(['es'])
        print('successfully created restaurant topic')
    except:
        print('fail to create restaurant topic')
        pass
print('test')
for message in consumer:
    print("restuanrt for loop")
    new_listing = json.loads((message.value).decode('utf-8'))
    print(new_listing)
    es.index(index='restaurant_index', doc_type='listing', id=new_listing['id'], body=new_listing)
    es.indices.refresh(index='restaurant_index')
