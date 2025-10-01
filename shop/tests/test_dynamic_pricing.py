from decimal import Decimal
from django.test import TestCase
from shop.models import Product

class DynamicPricingTests(TestCase):
    def setUp(self):
        self.p = Product.objects.create(
            name="Phone",
            price=Decimal("100.00"),
            quantity=50,
            initial_quantity=50,
            sold_count=0
        )

    def test_sell_decreases_quantity(self):
        self.p.sell(3)
        self.p.refresh_from_db()
        self.assertEqual(self.p.quantity, 47)
        self.assertEqual(self.p.sold_count, 3)
        self.assertEqual(self.p.price, Decimal("100.00"))  # пока порог не достигнут

    def test_price_bumps_on_10th(self):
        self.p.sell(9)
        self.p.sell(1)  # 10-я продажа → повышение
        self.p.refresh_from_db()
        self.assertEqual(self.p.sold_count, 10)
        self.assertEqual(self.p.quantity, 40)
        self.assertEqual(self.p.price, Decimal("115.00"))

    def test_price_bumps_on_every_10(self):
        self.p.sell(10)  # bump #1 -> 115.00
        self.p.sell(10)  # bump #2 -> 132.25
        self.p.refresh_from_db()
        self.assertEqual(self.p.sold_count, 20)
        self.assertEqual(self.p.quantity, 30)
        self.assertEqual(self.p.price, Decimal("132.25"))

    def test_multi_threshold_in_one_go(self):
        self.p.sell(20)  # за один вызов пересекли 2 порога
        self.p.refresh_from_db()
        self.assertEqual(self.p.sold_count, 20)
        self.assertEqual(self.p.quantity, 30)
        self.assertEqual(self.p.price, Decimal("132.25"))
