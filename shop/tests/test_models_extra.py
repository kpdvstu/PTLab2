from decimal import Decimal
from django.test import TestCase
from shop.models import Product


class ProductExtraTests(TestCase):
    def setUp(self):
        self.p = Product.objects.create(
            name="TestProduct",
            price=Decimal("100.00"),
            quantity=10,
            initial_quantity=10,
            sold_count=0
        )

    def test_cannot_sell_more_than_in_stock(self):
        with self.assertRaises(ValueError):
            self.p.sell(20)

    def test_cannot_sell_zero_or_negative(self):
        with self.assertRaises(ValueError):
            self.p.sell(0)
        with self.assertRaises(ValueError):
            self.p.sell(-3)

    def test_price_rounding_to_two_decimals(self):
        self.p.price = Decimal("99.9999")
        self.p.save()
        self.p.sell(10)  # пересекаем порог
        self.p.refresh_from_db()
        self.assertEqual(self.p.price, Decimal("115.00"))
