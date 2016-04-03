from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json

consumer = None
es = None

while not consumer or not es:
	try:
		consumer  = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
		es = Elasticsearch(['es'])
	except:
		pass
print('test')
for message in consumer:
	print("in reservation for loop")
	new_listing = json.loads((message.value).decode('utf-8'))
	print(new_listing)
	# customer_id = new_listing['customer_id']
	# table_id = new_listing['table']
	# reservation_id = new_listing['reservation_id']
	# start_time = new_listing['start_time']
	# end_time = new_listing['end_time']
	# created_time = new_listing['created_time']
	# restaurant_name = new_listing['restaurant_name']
	# some_new_listing = { 'customer_id':customer_id, 'table_id':table_id,'start_time':start_time, 'end_time': end_time, 'created_time':created_time, 'restaurant_name':restaurant_name}
	es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing)
	es.indices.refresh(index='listing_index')
