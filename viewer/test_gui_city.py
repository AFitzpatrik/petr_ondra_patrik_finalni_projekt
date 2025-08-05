import time
from django.contrib.auth.models import User
from django.test import LiveServerTestCase, Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from viewer.models import Country, City


class CityFormGUITest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        cls.browser = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.country = Country.objects.create(name = "Czech Republic")

        self.user = User.objects.create_superuser(username="Nunu", password="test123")
        self.client = Client()
        self.client.login(username="Nunu", password="test123")
        sessionid = self.client.cookies["sessionid"].value

        self.browser.get(f"{self.live_server_url}/404/")
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        self.browser.add_cookie({
            "name": "sessionid",
            "value": sessionid,
            "path": "/",
            "domain": "localhost",
        })


    def fill_and_submit_form(self, name, zip_code):
        self.browser.get(f"{self.live_server_url}/city/create/")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )

        self.browser.find_element(By.NAME, "name").send_keys(name)
        time.sleep(3)

        select_element = self.browser.find_element(By.NAME, "country")
        Select(select_element).select_by_visible_text("Czech Republic")
        time.sleep(3)

        self.browser.find_element(By.NAME, "zip_code").send_keys(zip_code)
        time.sleep(3)

        self.browser.find_element(By.ID, "city-form").submit()
        time.sleep(5)

    def test_submit_city_twice_show_validation_error(self):
        print("-" * 80)
        print(f"Spouští se test: test_submit_city_twice_show_validation_error")

        self.fill_and_submit_form("hluBoká NAD vLtavou", "444444")
        self.assertIn("PSČ musí obsahovat 4 nebo 5 čísel bez mezer a pomlček.", self.browser.page_source)

        self.fill_and_submit_form("hluBoká NAD vLtavou", "44444")
        self.assertNotIn("Město s tímhle názvem a PSČ již v tomto státě existuje.", self.browser.page_source)

        self.fill_and_submit_form("HluboKá nad VLtavou", "44444")
        self.assertIn("Město s tímhle názvem a PSČ již v tomto státě existuje.", self.browser.page_source)



