from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase


class HomePageTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        pass

    def get_full_url(self, namespace):
        local_server_url = "http://192.168.99.100:8000"  # CHANGE THIS TO YOUR WEB URL
        # return self.live_server_url + reverse(namespace)
        return local_server_url + reverse(namespace)

    def test_home_title(self):
        self.browser.get(self.get_full_url("homepage"))
        self.assertIn("Tabook", self.browser.title)

    def test_h1_css(self):
        self.browser.get(self.get_full_url("homepage"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"),
                         "rgba(37, 33, 34, 1)")


class SearchBarTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        pass

    def get_full_url(self, namespace):
        local_server_url = "http://192.168.99.100:8000"  # CHANGE THIS TO YOUR WEB URL
        # return self.live_server_url + reverse(namespace)
        return local_server_url + reverse(namespace)

    def test_search_bar_is_on_homepage(self):
        self.browser.get(self.get_full_url("homepage"))
        # fill in the form and type "somewhere" in the search bar and submit the form
        element = self.browser.find_element_by_name("query")
        self.assertIsNotNone(element)

    def test_search_on_homepage(self):
        self.browser.get(self.get_full_url("homepage"))
        # fill in the form and type "somewhere" in the search bar and submit the form
        element = self.browser.find_element_by_name("query")
        element.send_keys("somewhere")
        element.submit()
        # it should to the search result page
        self.assertHTMLEqual(self.browser.current_url, self.get_full_url("restaurant_list") + "?query=somewhere")
        # there is a restaurant with address "somewhere"
        restaurant_boxes = self.browser.find_elements_by_class_name("restaurant-box")
        for restaurant_box in restaurant_boxes:
            # print(str(restaurant_box.text))
            self.assertIn("somewhere", restaurant_box.text)
