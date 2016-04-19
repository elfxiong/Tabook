from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase


# class HomePageTest(LiveServerTestCase):
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(3)
#
#     def tearDown(self):
#         self.browser.quit()
#         pass
#
#     def get_full_url(self, namespace):
#         local_server_url = "http://192.168.99.100:8000"  # CHANGE THIS TO YOUR WEB URL
#         # return self.live_server_url + reverse(namespace)
#         return local_server_url + reverse(namespace)
#
#     def test_home_title(self):
#         self.browser.get(self.get_full_url("homepage"))
#         self.assertIn("Tabook", self.browser.title)
#
#     def test_h1_css(self):
#         self.browser.get(self.get_full_url("homepage"))
#         h1 = self.browser.find_element_by_tag_name("h1")
#         self.assertEqual(h1.value_of_css_property("color"),
#                          "rgba(37, 33, 34, 1)")
#
#
# class SearchBarTest(LiveServerTestCase):
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(3)
#
#     def tearDown(self):
#         self.browser.quit()
#         pass
#
#     def get_full_url(self, namespace):
#         local_server_url = "http://192.168.99.100:8000"  # CHANGE THIS TO YOUR WEB URL
#         # return self.live_server_url + reverse(namespace)
#         return local_server_url + reverse(namespace)
#
#     def test_search_bar_is_on_homepage(self):
#         self.browser.get(self.get_full_url("homepage"))
#         # fill in the form and type "somewhere" in the search bar and submit the form
#         element = self.browser.find_element_by_name("query")
#         self.assertIsNotNone(element)
#
#     def test_search_on_homepage(self):
#         self.browser.get(self.get_full_url("homepage"))
#         # fill in the form and type "somewhere" in the search bar and submit the form
#         element = self.browser.find_element_by_name("query")
#         element.send_keys("somewhere")
#         element.submit()
#         # it should to the search result page
#         self.assertHTMLEqual(self.browser.current_url, self.get_full_url("restaurant_list") + "?query=somewhere")
#         # there is a restaurant with address "somewhere"
#         restaurant_boxes = self.browser.find_elements_by_class_name("restaurant-box")
#         for restaurant_box in restaurant_boxes:
#             # print(str(restaurant_box.text))
#             self.assertIn("somewhere", restaurant_box.text)
#
#
# class AuthTest(LiveServerTestCase):
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(3)
#
#     def tearDown(self):
#         self.browser.quit()
#         pass
#
#     def get_full_url(self, namespace):
#         local_server_url = "http://192.168.99.100:8000"  # CHANGE THIS TO YOUR WEB URL
#         # return self.live_server_url + reverse(namespace)
#         return local_server_url + reverse(namespace)
#
#     def test_login(self):
#         self.browser.get(self.get_full_url("homepage"))
#         # log in
#         element = self.browser.find_element_by_name("login_page")
#         element.click()
#         username_field = self.browser.find_element_by_name("username")
#         username_field.send_keys("admin")
#         password_field = self.browser.find_element_by_name("password")
#         password_field.send_keys("adminpassword")
#         submit_button = self.browser.find_element_by_id("submit_button")
#         submit_button.submit()
#         logout_link = self.browser.find_element_by_name("logout_page")
#         self.assertIsNotNone(logout_link)
#
#     def test_logout(self):
#         self.browser.get(self.get_full_url("homepage"))
#         # log in
#         element = self.browser.find_element_by_name("login_page")
#         element.click()
#         username_field = self.browser.find_element_by_name("username")
#         username_field.send_keys("admin")
#         password_field = self.browser.find_element_by_name("password")
#         password_field.send_keys("adminpassword")
#         submit_button = self.browser.find_element_by_id("submit_button")
#         submit_button.submit()
#         logout_link = self.browser.find_element_by_name("logout_page")
#         logout_link.click()
#         login_link = self.browser.find_element_by_name("login_page")
#         self.assertIsNotNone(login_link)
#
#
# class RestaurantDetailsPageTest(LiveServerTestCase):
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.browser.implicitly_wait(3)
#
#     def tearDown(self):
#         self.browser.quit()
#         pass
#
#     def logIn(self):
#         self.browser.get(self.get_full_url("homepage"))
#         # log in
#         element = self.browser.find_element_by_name("login_page")
#         element.click()
#         username_field = self.browser.find_element_by_name("username")
#         username_field.send_keys("admin")
#         password_field = self.browser.find_element_by_name("password")
#         password_field.send_keys("adminpassword")
#         submit_button = self.browser.find_element_by_id("submit_button")
#         submit_button.submit()
#
#     def get_full_url(self, namespace):
#         local_server_url = "http://192.168.99.100:8000"  # CHANGE THIS TO YOUR WEB URL
#         # return self.live_server_url + reverse(namespace)
#         return local_server_url + reverse(namespace)
#
#     def test_go_to_restaurant_details(self):
#         self.browser.get(self.get_full_url("homepage"))
#         self.logIn()
#         restaurant_details_link = self.browser.find_element_by_name("details_link_Starbucks")
#         restaurant_details_link.click()
#         # redirect to restaurant_details_page
#         restaurant_name = self.browser.find_element_by_id("restaurant_name")
#         self.assertTrue(restaurant_name.text == "Starbucks")
#
#     def test_address_in_restaurant_details(self):
#         self.browser.get(self.get_full_url("homepage"))
#         self.logIn()
#         restaurant_details_link = self.browser.find_element_by_name("details_link_Starbucks")
#         restaurant_details_link.click()
#         # redirect to restaurant_details_page
#         restaurant_name = self.browser.find_element_by_id("restaurant_name")
#         self.assertTrue(restaurant_name.text == "Starbucks")
#         address = self.browser.find_element_by_id("Address")
#         self.assertIn("Address", address.text)


class ReservationHistoryTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        pass

    def logIn(self):
        self.browser.get(self.get_full_url("homepage"))
        # log in
        element = self.browser.find_element_by_name("login_page")
        element.click()
        username_field = self.browser.find_element_by_name("username")
        username_field.send_keys("admin")
        password_field = self.browser.find_element_by_name("password")
        password_field.send_keys("adminpassword")
        submit_button = self.browser.find_element_by_id("submit_button")
        submit_button.submit()

    def get_full_url(self, namespace):
        local_server_url = "http://192.168.99.100:8000"  # CHANGE THIS TO YOUR WEB URL
        # return self.live_server_url + reverse(namespace)
        return local_server_url + reverse(namespace)

    def test_login_go_to_reservation_history(self):
        self.browser.get(self.get_full_url("homepage"))
        self.logIn()
        reservations_link = self.browser.find_element_by_name("reservation_history_page")
        reservations_link.click()
        reservation_history_title = self.browser.find_element_by_name("title")
        self.assertIsNotNone(reservation_history_title)

    def test_search_bar_on_reservation_history(self):
        pass

    def test_search_existing_reservations(self):
        pass