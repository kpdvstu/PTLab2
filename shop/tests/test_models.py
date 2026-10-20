from django.test import TestCase
from shop.models import Product

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price=740, category="Книги")
        Product.objects.create(name="pencil", price=50, category="Канцелярия")

    def test_correctness_types(self):                   
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, int)

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="book").price == 740)