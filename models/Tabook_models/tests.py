from django.test import TestCase, Client
from .models import Customer, Restaurant, Table, Review
import json


class CustomerAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Customer.objects.create(username="lion", password="roar", email="roar@lion.zoo", phone="55555")
        Customer.objects.create(username="cat", password="meow", email="meow@cat.zoo", phone="333")

    def test_create_customer_fail(self):
        response = self.client.post('/api/customers/create/')
        expected_json = {"success": False,
                         "html": {"password": ["This field is required."], "username": ["This field is required."]},
                         "result": "Form is invalid. Failed to create a new customer"}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_create_customer_succeed(self):
        post_data = {'username': 'bear', 'password': 'waa'}
        response = self.client.post('/api/customers/create/', data=post_data)
        expected_json = {'user': {'type': 'C', 'id': 3}, 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_get_customer_succeed_1(self):
        response = self.client.get('/api/customers/1/')
        expected_json = {'result': {'email': 'roar@lion.zoo',
                                    'id': 1,
                                    'phone': '55555',
                                    'username': 'lion'},
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_get_customer_succeed_2(self):
        response = self.client.get('/api/customers/2/')
        expected_json = {'result': {'email': 'meow@cat.zoo',
                                    'id': 2,
                                    'phone': '333',
                                    'username': 'cat'},
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_get_customer_with_nonexistant_id(self):
        response = self.client.get('/api/customers/3/')
        expected_json = {'result': 'Customer not found', 'success': False}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_update_customer_info_without_id(self):
        response = self.client.post('/api/customers/update/')
        expected_json = {'result': 'Customer id not provided', 'success': False}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_update_customer_info(self):
        # change only email field
        post_data = {'id': 1, 'email': 'roar2@lion.zoo'}
        response = self.client.post('/api/customers/update/', post_data)
        expected_json = {'changed': ['email'], 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)
        # see if the email field is updated
        response = self.client.get('/api/customers/1/')
        expected_json = {'result': {'email': 'roar2@lion.zoo',
                                    'id': 1,
                                    'phone': '55555',
                                    'username': 'lion'},
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)


class RestaurantAPITestCase(TestCase):
    def setUp(self):
        self.factory = Client()
        c = Customer.objects.create(username="user", password="pass", email="user@user.com", phone="00000")
        r1 = Restaurant.objects.create(username="lion", password="roar", email="roar@lion.zoo", phone="55555")
        r2 = Restaurant.objects.create(username="cat", password="meow", email="meow@cat.zoo", phone="333")

    def test_create_restaurant(self):
        post_data = {'username': 'myrestaurant', 'password': 'pas', 'restaurant_name': 'Tabook Restaurant',
                     'address': "123 lane", 'price_range': 1, 'category': 'Italian'}
        response = self.factory.post('/api/restaurants/create/', post_data)
        expected_data = {'success': True, 'user': {'id': 3, 'type': 'R'}}

        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    # def test_get_restaurant(self):
    #     pass

    def test_update_restaurant_address(self):
        post_data = {'id': 1, 'address': '10 sucessful change dr'}
        response = self.factory.post('/api/restuarants/update', post_data)
        expected_data = {"success": True, "changed": "address"}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    def test_update_restaurant_phone_bad(self):
        post_data = {'id': 1, 'phone': 'bad phone'}
        response = self.factory.post('/api/restuarants/update', post_data)
        expected_data = {"success": False, "changed": "address"}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    def test_filter_restaurant_with_no_parameter(self):
        # expected to get all restaurants
        get_data = {}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [{'address': 'unknown',
                                     'email': 'roar@lion.zoo',
                                     'id': 1,
                                     'phone': '55555',
                                     'restaurant_name': 'anonymous',
                                     'username': 'lion'},
                                    {'address': 'unknown',
                                     'email': 'meow@cat.zoo',
                                     'id': 2,
                                     'phone': '333',
                                     'restaurant_name': 'anonymous',
                                     'username': 'cat'}],
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_username(self):  # should be changed to something relevant to our app
        get_data = {'username': 'lion'}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [{'address': 'unknown',
                                     'email': 'roar@lion.zoo',
                                     'id': 1,
                                     'phone': '55555',
                                     'restaurant_name': 'anonymous',
                                     'username': 'lion'}],
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_phone(self):
        get_data = {'phone': '55555'}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [{'address': 'unknown',
                                     'email': 'roar@lion.zoo',
                                     'id': 1,
                                     'phone': '55555',
                                     'restaurant_name': 'anonymous',
                                     'username': 'lion'}],
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_email_and_phone(self):
        get_data = {'email': 'roar@lion.zoo', 'phone': '55555'}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [{'address': 'unknown',
                                     'email': 'roar@lion.zoo',
                                     'id': 1,
                                     'phone': '55555',
                                     'restaurant_name': 'anonymous',
                                     'username': 'lion'}],
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_nonexistant_username(self):
        get_data = {'username': 'bear'}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [], 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_create_review_successful(self):
        post_data = {'customer_id': 1, 'restaurant_id': 1,
                     'stars': "5", 'text': 'great food'}
        response = self.factory.post('/api/restaurants/reviews/create/', post_data)

        expected_data = {"success": True, 'id': 1}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    def test_get_reviews_single(self):
        Review.objects.create(customer=Customer.objects.get(id=1), restaurant=Restaurant.objects.get(id=1),
                              stars=5, text='great food')
        get_data = {'restaurant_id': '1'}
        response = self.factory.get('/api/restaurants/reviews/', get_data)
        response_json = json.loads(str(response.content, encoding='utf-8'))
        response_json['result'][0]['created'] = '0'  # reset date field b/c untestable
        expected_json = {'result': [{'customer_id': 1, 'text': 'great food', 'created': '0', 'stars': 5, 'id': 1}],
                         'success': True}
        self.assertDictEqual(response_json, expected_json)


class TableAPITestCase(TestCase):
    def setUp(self):
        self.factory = Client()
        r1 = Restaurant.objects.create(username="lion", password="roar", email="roar@lion.zoo", phone="55555")
        r2 = Restaurant.objects.create(username="cat", password="meow", email="meow@cat.zoo", phone="333")
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

    def test_filter_table_1(self):
        get_data = {'restaurant_id': 1}
        response = self.factory.get('/api/tables/filter/', get_data)
        # print(str(response.content, encoding='utf8'))
        expected_data = {"success": True, "result": [
            {"x_coordinate": None, "capacity": 4, "id": 1, "y_coordinate": None, "style": "unspecified",
             "restaurant": 1},
            {"x_coordinate": None, "capacity": 4, "id": 2, "y_coordinate": None, "style": "unspecified",
             "restaurant": 1},
            {"x_coordinate": None, "capacity": 3, "id": 3, "y_coordinate": None, "style": "unspecified",
             "restaurant": 1},
            {"x_coordinate": None, "capacity": 3, "id": 4, "y_coordinate": None, "style": "unspecified",
             "restaurant": 1},
            {"x_coordinate": None, "capacity": 3, "id": 5, "y_coordinate": None, "style": "unspecified",
             "restaurant": 1}]}

        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    def test_filter_table_2(self):
        get_data = {'restaurant_id': 2}
        response = self.factory.get('/api/tables/filter/', get_data)
        expected_data = {"success": True, "result": [
            {"id": 6, "restaurant": 2, "style": "unspecified", "capacity": 3, "y_coordinate": None,
             "x_coordinate": None},
            {"id": 7, "restaurant": 2, "style": "unspecified", "capacity": 3, "y_coordinate": None,
             "x_coordinate": None},
            {"id": 8, "restaurant": 2, "style": "unspecified", "capacity": 3, "y_coordinate": None,
             "x_coordinate": None},
            {"id": 9, "restaurant": 2, "style": "unspecified", "capacity": 2, "y_coordinate": None,
             "x_coordinate": None},
            {"id": 10, "restaurant": 2, "style": "unspecified", "capacity": 2, "y_coordinate": None,
             "x_coordinate": None}]}

        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)
