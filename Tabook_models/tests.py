from django.test import TestCase, Client
from .models import Customer, Restaurant, Table


class CustomerAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Customer.objects.create(username="lion", password="roar", email="roar@lion.zoo", phone="55555")
        Customer.objects.create(username="cat", password="meow", email="meow@cat.zoo", phone="333")

    def test_create_customer_fail(self):
        response = self.client.post('/api/customers/create/')
        expected_json = {"success": False,
                         "html": {"password": ["This field is required."], "username": ["This field is required."]},
                         "result": "Failed to create a new customer"}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_create_customer_succeed(self):
        post_data = {'username': 'bear', 'password': 'waa'}
        response = self.client.post('/api/customers/create/', data=post_data)
        expected_json = {"id": 3, "success": True}
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
        Restaurant.objects.create(username="lion", password="roar", email="roar@lion.zoo", phone="55555")
        Restaurant.objects.create(username="cat", password="meow", email="meow@cat.zoo", phone="333")

    def test_create_restaurant(self):
        post_data = {'username': 'myrestaurant', 'password': 'pas', 'restaurant_name': 'Tabook Restaurant',
                     'address': "123 lane", 'price_range': 1, 'category': 'Italian'}
        response = self.factory.post('/api/restaurants/create/', post_data)
        expected_data = {"success": True, 'id': 3}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    def test_get_restaurant(self):
        pass

    def test_update_restaurant(self):
        pass

    def test_filter_restaurant_with_no_parameter(self):
        # expected to get all restaurants
        get_data = {}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [{'address': '',
                                     'email': 'roar@lion.zoo',
                                     'id': 1,
                                     'phone': '55555',
                                     'restaurant_name': '',
                                     'username': 'lion'},
                                    {'address': '',
                                     'email': 'meow@cat.zoo',
                                     'id': 2,
                                     'phone': '333',
                                     'restaurant_name': '',
                                     'username': 'cat'}],
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_username(self):  # should be changed to something relevant to our app
        get_data = {'username': 'lion'}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [{'address': '',
                                     'email': 'roar@lion.zoo',
                                     'id': 1,
                                     'phone': '55555',
                                     'restaurant_name': '',
                                     'username': 'lion'}],
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_phone(self):
        get_data = {'phone': '55555'}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [{'address': '',
                                     'email': 'roar@lion.zoo',
                                     'id': 1,
                                     'phone': '55555',
                                     'restaurant_name': '',
                                     'username': 'lion'}],
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_email_and_phone(self):
        get_data = {'email': 'roar@lion.zoo', 'phone': '55555'}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [{'address': '',
                                     'email': 'roar@lion.zoo',
                                     'id': 1,
                                     'phone': '55555',
                                     'restaurant_name': '',
                                     'username': 'lion'}],
                         'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_nonexistant_username(self):
        get_data = {'username': 'bear'}
        response = self.factory.get('/api/restaurants/filter/', get_data)
        expected_json = {'result': [], 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)


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
            {"x_coordinate": None, "y_coordinate": None, "restaurant_id": 1, "capacity": 4, "id": 1,
             "style": "unspecified"},
            {"x_coordinate": None, "y_coordinate": None, "restaurant_id": 1, "capacity": 4, "id": 2,
             "style": "unspecified"},
            {"x_coordinate": None, "y_coordinate": None, "restaurant_id": 1, "capacity": 3, "id": 3,
             "style": "unspecified"},
            {"x_coordinate": None, "y_coordinate": None, "restaurant_id": 1, "capacity": 3, "id": 4,
             "style": "unspecified"},
            {"x_coordinate": None, "y_coordinate": None, "restaurant_id": 1, "capacity": 3, "id": 5,
             "style": "unspecified"}]}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    def test_filter_table_2(self):
        get_data = {'restaurant_id': 2}
        response = self.factory.get('/api/tables/filter/', get_data)
        expected_data = {"success": True, "result": [
            {"style": "unspecified", "id": 6, "y_coordinate": None, "capacity": 3, "x_coordinate": None,
             "restaurant_id": 2},
            {"style": "unspecified", "id": 7, "y_coordinate": None, "capacity": 3, "x_coordinate": None,
             "restaurant_id": 2},
            {"style": "unspecified", "id": 8, "y_coordinate": None, "capacity": 3, "x_coordinate": None,
             "restaurant_id": 2},
            {"style": "unspecified", "id": 9, "y_coordinate": None, "capacity": 2, "x_coordinate": None,
             "restaurant_id": 2},
            {"style": "unspecified", "id": 10, "y_coordinate": None, "capacity": 2, "x_coordinate": None,
             "restaurant_id": 2}]}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)
