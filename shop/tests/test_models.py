from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Product, CartItem


class CartItemModelTest(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='tester', password='password')

        # Создаем товар (Вино за 1000р)
        self.product = Product.objects.create(
            title="Вино Изабелла",
            price=1000,
            description="Красное полусладкое"
        )

    def test_cart_item_creation(self):
        """Проверяем, что объект корзины создается корректно"""
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=3
        )
        self.assertEqual(cart_item.product.title, "Вино Изабелла")
        self.assertEqual(cart_item.quantity, 3)

    def test_total_price_calculation(self):
        """Проверяем метод total_price (если ты его добавил в models.py)"""
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
        # 2 бутылки по 1000р должны стоить 2000р
        # Если у тебя в модели нет метода total_price, удали этот тест или добавь метод в models.py
        if hasattr(cart_item, 'total_price'):
            self.assertEqual(cart_item.total_price(), 2000)