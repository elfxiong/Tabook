from django.test import TestCase, RequestFactory
from .models import Customer
from .main import create_customer


class CustomerAPITestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Customer.objects.create(username="lion", password="roar", email="roar@lion.zoo", phone="55555")
        Customer.objects.create(username="cat", password="meow", email="meow@cat.zoo", phone="333")

    def test_create_customer(self):
        # failure case
        request = self.factory.post('/customer/create/')
        response = create_customer(request)
        expected_json = {"success": False,
                         "html": {"password": ["This field is required."], "username": ["This field is required."]},
                         "result": "Failed to create a new customer"}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

        # success case
        post_data = {'username': 'bear', 'password': 'waa'}
        request = self.factory.post('/customer/create/', data=post_data)
        response = create_customer(request)
        expected_json = {"id": 3, "success": True}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_json)

        # print(str(response.content, encoding='utf8')) # print to see actual response

    def test_get_customer(self):
        pass

    def test_update_customer_info(self):
        pass
