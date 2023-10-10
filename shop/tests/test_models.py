from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime

class ProductModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="book", price=740, total_sold=0)

    def test_create_product(self):
        self.assertEqual(self.product.name, "book")
        self.assertEqual(self.product.price, 740)
        self.assertEqual(self.product.total_sold, 0)

    def test_price_increase(self):
        # Проверим, корректно ли увеличивается цена после каждой 10-й продажи
        initial_price = self.product.price
        
        for i in range(1, 12):  # 11 итераций, чтобы произошло одно увеличение цены
            self.product.total_sold += 1
            if self.product.total_sold % 10 == 0:
                self.product.price *= 1.25
            self.product.save()
            
            if i < 10:
                self.assertEqual(self.product.price, initial_price)  # Цена не должна измениться
            else:
                self.assertEqual(self.product.price, initial_price * 1.25)  # Цена должна увеличиться на 25%
            self.assertEqual(self.product.total_sold, i)

