from kafka import KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers='kafka:9092')
some_new_listing = { 'customer_id':'0', 'table_id':'0', 'start_time': '0', 'end_time' : '0', 'created_time':'0'}
producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
