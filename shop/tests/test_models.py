from django.test import TestCase
from shop.models import Product, Purchase, Discount
from datetime import datetime

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

class DiscountTestCase(TestCase):
    def setUp(self):
        Discount.objects.create(person="user_1", total="1000", discount="0.1")
        Discount.objects.create(person="user_2", total="20000", discount="2.0")
        Discount.objects.create(person="user_3", total="2000000", discount="25")

    def test_correctness_types(self):
        self.assertIsInstance(Discount.objects.get(person="user_1").person, str)
        self.assertIsInstance(Discount.objects.get(person="user_1").total, int)
        self.assertIsInstance(Discount.objects.get(person="user_1").discount, float)
        self.assertIsInstance(Discount.objects.get(person="user_2").person, str)
        self.assertIsInstance(Discount.objects.get(person="user_2").total, int)
        self.assertIsInstance(Discount.objects.get(person="user_2").discount, float)
        self.assertIsInstance(Discount.objects.get(person="user_3").person, str)
        self.assertIsInstance(Discount.objects.get(person="user_3").total, int)
        self.assertIsInstance(Discount.objects.get(person="user_3").discount, float)

    def test_correctness_data(self):
        self.assertTrue(Discount.objects.get(person="user_1").total == 1000)
        self.assertTrue(Discount.objects.get(person="user_1").discount == 0.1)
        self.assertTrue(Discount.objects.get(person="user_2").total == 20000)
        self.assertTrue(Discount.objects.get(person="user_2").discount == 2.0)
        self.assertTrue(Discount.objects.get(person="user_3").total == 2000000)
        self.assertTrue(Discount.objects.get(person="user_3").discount == 25)