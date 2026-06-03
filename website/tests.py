from django.test import TestCase
from django.urls import reverse


class WebsitePagesTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_api_home_loads(self):
        response = self.client.get(reverse("api_home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "BKLN-TECH API")
