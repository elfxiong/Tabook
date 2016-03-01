from django.test import SimpleTestCase, Client
import json


class RestaurantAPITest(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_create_restaurant(self):
        post_data = {'username': 'myrestaurant', 'password': 'pas', 'restaurant_name': 'Tabook Restaurant', 'address': "123 lane", 'price_range': 1, 'category': 'Italian'}
        response = self.client.post('/restaurants/create/', post_data)
        expected_json = {'id': 1, 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)
