from django.test import TestCase
from django.core.management import call_command
from shop.models import Product


class FixturesTests(TestCase):
    def test_products_fixture_loads(self):
        call_command("loaddata", "products.yaml", verbosity=0)
        products = Product.objects.all()
        self.assertGreaterEqual(products.count(), 3)
