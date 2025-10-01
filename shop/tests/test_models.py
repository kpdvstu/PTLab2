from django.test import TestCase
from shop.models import Product
from decimal import Decimal

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price=Decimal("740.00"))
        Product.objects.create(name="pencil", price=Decimal("50.00"))

    def test_correctness_types(self):
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, Decimal)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, Decimal)

    def test_correctness_data(self):
        self.assertEqual(Product.objects.get(name="book").price, Decimal("740.00"))
        self.assertEqual(Product.objects.get(name="pencil").price, Decimal("50.00"))



#class PurchaseTestCase(TestCase):
#    def setUp(self):
#        self.product_book = Product.objects.create(name="book", price="740")
#        self.datetime = datetime.now()
#        Purchase.objects.create(product=self.product_book,
#                                person="Ivanov",
#                                address="Svetlaya St.")
#
#    def test_correctness_types(self):
#        self.assertIsInstance(Purchase.objects.get(product=self.product_book).person, str)
#        self.assertIsInstance(Purchase.objects.get(product=self.product_book).address, str)
#        self.assertIsInstance(Purchase.objects.get(product=self.product_book).date, datetime)
#
#    def test_correctness_data(self):
#        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Ivanov")
#        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "Svetlaya St.")
#        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) == \
#            self.datetime.replace(microsecond=0))