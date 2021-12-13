from django.test import TestCase
from shop.models import Product, Purchase, User
from datetime import datetime


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(sum=0.0)
        User.objects.create(name=1000.0)
        User.objects.create(name=10000.0)
        User.objects.create(name=100000.0)
        User.objects.create(name=1000000.0)
        User.objects.create(name=10000000.0)

    def test_correctness_types(self):
        self.assertIsInstance(User.objects.get(sum=0.0).sum, float)
        self.assertIsInstance(User.objects.get(sum=1000.0).sum, float)
        self.assertIsInstance(User.objects.get(sum=10000.0).sum, float)
        self.assertIsInstance(User.objects.get(sum=100000.0).sum, float)
        self.assertIsInstance(User.objects.get(sum=1000000.0).sum, float)
        self.assertIsInstance(User.objects.get(sum=10000000.0).sum, float)

    def test_correctness_data(self):
        self.assertTrue(User.objects.get(sum=0.0).sum == 0.0)
        self.assertTrue(User.objects.get(sum=1000.0).sum == 1000.0)
        self.assertTrue(User.objects.get(sum=10000.0).sum == 10000.0)
        self.assertTrue(User.objects.get(sum=100000.0).sum == 100000.0)
        self.assertTrue(User.objects.get(sum=1000000.0).sum == 1000000.0)
        self.assertTrue(User.objects.get(sum=10000000.0).sum == 1000000.0)

        self.assertTrue(User.objects.get(sum=0.0).discount == 0)
        self.assertTrue(User.objects.get(sum=1000.0).discount == 1)
        self.assertTrue(User.objects.get(sum=10000.0).discount == 2)
        self.assertTrue(User.objects.get(sum=100000.0).discount == 5)
        self.assertTrue(User.objects.get(sum=1000000.0).discount == 10)
        self.assertTrue(User.objects.get(sum=10000000.0).discount == 25)


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price="740")
        Product.objects.create(name="pencil", price="50")

    def test_correctness_types(self):
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, int)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, int)

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="book").price == 740)
        self.assertTrue(Product.objects.get(name="pencil").price == 50)


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="book", price="740")
        self.datetime = datetime.now()
        Purchase.objects.create(product=self.product_book,
                                person="Ivanov",
                                address="Svetlaya St.")

    def test_correctness_types(self):
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).person, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).address, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).date, datetime)

    def test_correctness_data(self):
        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Ivanov")
        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "Svetlaya St.")
        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) == \
                        self.datetime.replace(microsecond=0))
