from django.test import LiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import WebDriverException

from django.contrib.auth.models import User

from menu.models import Menu, Item, Ingredient 

import time
from django.utils import timezone

MAX_WAIT = 10

user = User.objects.get(id=1)
class NewVisitorTest(LiveServerTestCase):
    """basically runs through the website using the browser
    to see if its working"""
    def setUp(self):
        """establishes a model instance in the database"""
        self.browser = webdriver.Firefox()

        self.ingredient = Ingredient.objects.create(
            name="lskdjflkjfd"
            )
        self.item = Item(
                name="LKJklsjd",
            description="LKSJdlfkjsldfjsd",
            chef=user,
            )
        self.item.save()
        self.item.ingredients.add(self.ingredient)
        
        self.menu = Menu(
            season="asdfasdfadsfadsf",
            expiration_date=timezone.now() + timezone.timedelta(days=1)
            )
        self.menu.save()
        self.menu.items.add(self.item)
    def tearDown(self):
        self.browser.quit()

    # notice how this one doesn't start with 'test',
    # that's because it is a helper method to keep our code DRY. 
    def solve_loading_interference(
        self, specific_text, specific_text_not="hippo"):
        """is a method instead of doing 'time.sleep()'"""
        #we set this up so not only do we not have to use a 'time.sleep()'
        #to let the browser load, we catch the browser when it loads
        #within a half second which cuts down on wait time to finish the testing.
        #you have to do a time.wait type of maneuver after whenever you do
        #input.send_keys.(Keys.ENTER) or click()
        start_time = time.time()
        while True:
            try:
                page_text = self.browser.find_element_by_tag_name('body').text 
                self.assertIn(specific_text, page_text)
                self.assertNotIn(specific_text_not, page_text)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e 
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """runs through the browser to make sure site is working"""
        
        self.browser.get(self.live_server_url)
        body_text = self.browser.find_element_by_tag_name('body').text 
        self.assertIn("asdfasdfadsfadsf", body_text)

        anchors = self.browser.find_elements_by_tag_name('a')
        for anchor in anchors:
            if anchor.text == "asdfasdfadsfadsf":
                anchorA = anchor 
                break 
        anchorA.click()
        self.solve_loading_interference("On the menu this season:")

        edit_menu = self.browser.find_element_by_class_name('btn')
        edit_menu.click()
        self.solve_loading_interference("Change menu")

        edit_menu = self.browser.find_element_by_class_name('btn')
        edit_menu.click()
        self.solve_loading_interference("On the menu this season:")

        anchors = self.browser.find_elements_by_tag_name('a')
        for anchor in anchors:
            if anchor.text == "LKJklsjd":
                anchorA = anchor 
                break 
        anchorA.click()
        self.solve_loading_interference("lskdjflkjfd")

        anchors = self.browser.find_elements_by_tag_name('a')
        for anchor in anchors:
            if anchor.text == "Soda Fountain":
                anchorA = anchor 
                break 
        anchorA.click()
        self.solve_loading_interference("asdfasdfadsfadsf")

        new_menu = self.browser.find_element_by_class_name('top-menu')
        new_menu.click() 
        self.solve_loading_interference("Create new menu")

        inputbox = self.browser.find_element_by_id('id_season')
        inputbox.send_keys('best menu ever')
        checkbox = self.browser.find_element_by_id('id_items_0')
        checkbox.click()
        
        el = self.browser.find_element_by_id('id_expiration_date_year')
        for option in el.find_elements_by_tag_name('option'):
            if option.text == '2019':
                option.click() # select() in earlier versions of webdriver
                break
        submit_new_menu = self.browser.find_element_by_class_name('save')
        submit_new_menu.click()
        self.solve_loading_interference("On the menu this season")





        