from django.test import TestCase, Client
from shop.views import PurchaseCreate

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class DiscountCreateTestCase(TestCase):
        def setUp(self):
            self.client = Client()

        def test_webpage_accessibility(self):
            response = self.client.get('/discount/')
            self.assertEqual(response.status_code, 200)

        def test_webpage_not_found(self):
            response = self.client.get('discount/')
            self.assertEqual(response.status_code, 404)
