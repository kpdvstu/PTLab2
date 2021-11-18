from django.db.models.fields import DecimalField
from django.db.models.query_utils import select_related_descend
from django.test import TestCase
from shop.models import Product, Purchase
from datetime import date, datetime, timedelta
from decimal import *

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
        # Для проверки скидки на день рождения дата будет 1980 год, но текущий месяц и день
        Purchase.objects.create(product=self.product_book,
                                person="Ivanov Birthday",
                                address="Svetlaya St.",
                                birthday = date(1980, self.datetime.month, self.datetime.day),
                                discount=10,
                                sale_amount=10)

    def test_correctness_types(self):
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).person, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).address, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).date, datetime)
        # Наши новые поля
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).birthday, date)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).discount, Decimal)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).sale_amount, Decimal)

    def test_correctness_data(self):
        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Ivanov Birthday")
        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "Svetlaya St.")
        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) == \
        self.datetime.replace(microsecond=0))
        # Проверяем, что наши новые поля сохранются правильно
        self.assertTrue(Purchase.objects.get(product=self.product_book).birthday == date(1980, self.datetime.month, self.datetime.day))
        self.assertTrue(Purchase.objects.get(product=self.product_book).discount == Decimal('10'))
        self.assertTrue(Purchase.objects.get(product=self.product_book).sale_amount == Decimal('10'))
        