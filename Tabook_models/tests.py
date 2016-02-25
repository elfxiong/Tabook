from django.test import TestCase, RequestFactory
from .models import Customer, Restaurant
from .main import create_customer, update_customer, get_customer, filter_restaurant


class CustomerAPITestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Customer.objects.create(username="lion", password="roar", email="roar@lion.zoo", phone="55555")
        Customer.objects.create(username="cat", password="meow", email="meow@cat.zoo", phone="333")

    def test_create_customer_fail(self):
        request = self.factory.post('/customer/create/')  # the url does not need to be correct orz
        response = create_customer(request)
        expected_json = {"success": False,
                         "html": {"password": ["This field is required."], "username": ["This field is required."]},
                         "result": "Failed to create a new customer"}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_create_customer_succeed(self):
        post_data = {'username': 'bear', 'password': 'waa'}
        request = self.factory.post('/customer/create/', data=post_data)
        response = create_customer(request)
        expected_json = {"id": 3, "success": True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_get_customer_succeed_1(self):
        request = self.factory.get('/customers/1/')  # the url does not need to be correct orz
        response = get_customer(request, 1)
        expected_json = {'id': 1, 'username': 'lion', 'email': 'roar@lion.zoo', 'phone': '55555', 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_get_customer_succeed_2(self):
        request = self.factory.get('/customers/2/')
        response = get_customer(request, 2)
        expected_json = {'id': 2, 'username': 'cat', 'email': 'meow@cat.zoo', 'phone': '333', 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_get_customer_with_nonexistant_id(self):
        request = self.factory.get('/customers/3/')
        response = get_customer(request, 3)
        expected_json = {'result': 'Customer not found', 'success': False}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_update_customer_info_without_id(self):
        request = self.factory.post('/api/customers/update_customer/')
        response = update_customer(request)
        expected_json = {'result': 'Customer id not provided', 'success': False}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_update_customer_info(self):
        # change only email field
        post_data = {'id': 1, 'email': 'roar2@lion.zoo'}
        request = self.factory.post('/api/customers/update_customer/', post_data)
        response = update_customer(request)
        expected_json = {'changed': ['email'], 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)
        # see if the email field is updated
        request = self.factory.get('/api/custoemrs/1/')
        response = get_customer(request, 1)
        expected_json = {'id': 1, 'username': 'lion', 'email': 'roar2@lion.zoo', 'phone': '55555', 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)


class RestaurantAPITestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Restaurant.objects.create(username="lion", password="roar", email="roar@lion.zoo", phone="55555")
        Restaurant.objects.create(username="cat", password="meow", email="meow@cat.zoo", phone="333")

    def test_create_restaurant(self):
        pass

    def test_get_restaurant(self):
        pass

    def test_update_restaurant(self):
        pass

    def test_filter_restaurant_with_no_parameter(self):
        # expected to get all restaurants
        get_data = {}
        request = self.factory.get('/api/restaurants/filter/', get_data)
        response = filter_restaurant(request)
        expected_json = {'result': [{'id': 1, 'username': 'lion'}, {'id': 2, 'username': 'cat'}], 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_username(self):  # should be changed to something relevant to our app
        get_data = {'username': 'lion'}
        request = self.factory.get('/api/restaurants/filter/', get_data)
        response = filter_restaurant(request)
        expected_json = {'result': [{'id': 1, 'username': 'lion'}], 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_phone(self):
        get_data = {'phone': '55555'}
        request = self.factory.get('/api/restaurants/filter/', get_data)
        response = filter_restaurant(request)
        expected_json = {'result': [{'id': 1, 'username': 'lion'}], 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_email_and_phone(self):
        get_data = {'email': 'roar@lion.zoo', 'phone': '55555'}
        request = self.factory.get('/api/restaurants/filter/', get_data)
        response = filter_restaurant(request)
        expected_json = {'result': [{'id': 1, 'username': 'lion'}], 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

    def test_filter_restaurant_by_nonexistant_username(self):
        get_data = {'username': 'bear'}
        request = self.factory.get('/api/restaurants/filter/', get_data)
        response = filter_restaurant(request)
        expected_json = {'result': [], 'success': True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)
