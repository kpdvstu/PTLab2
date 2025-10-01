from django.test import TestCase
from django.urls import reverse
from shop.models import Product
from decimal import Decimal


class ShopViewsTests(TestCase):
    def setUp(self):
        Product.objects.create(name="Phone", price=Decimal("20000.00"), quantity=5)

    def test_index_page_loads(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phone")
        self.assertContains(response, "20000.00")

    def test_index_page_empty(self):
        Product.objects.all().delete()
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
