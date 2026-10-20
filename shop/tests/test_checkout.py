from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Order

class CheckoutDiscountTests(TestCase):
    def setUp(self):
        # Создаем тестовые товары разных категорий
        self.tshirt = Product.objects.create(name="Футболка", price=1000, category="Одежда")
        self.jeans = Product.objects.create(name="Джинсы", price=2000, category="Одежда")
        self.cap = Product.objects.create(name="Кепка", price=500, category="Головные уборы")
        
        self.client = Client()

    def test_no_discount_same_category(self):
        """Покупка товаров одной категории — скидка не применяется"""
        response = self.client.post(reverse('checkout'), {
            'person': 'Иван',
            'address': 'Москва',
            'products': [self.tshirt.id, self.jeans.id]
        })
        
        order = Order.objects.get(person='Иван')
        # 1000 + 2000 = 3000 (без скидки)
        self.assertEqual(order.total_price, 3000)

    def test_discount_different_categories(self):
        """Покупка товаров разных категорий — скидка 10% применяется"""
        response = self.client.post(reverse('checkout'), {
            'person': 'Петр',
            'address': 'Казань',
            'products': [self.tshirt.id, self.cap.id]
        })
        
        order = Order.objects.get(person='Петр')
        # 1000 + 500 = 1500, скидка 10% = 1350
        self.assertEqual(order.total_price, 1350)

    def test_single_product_no_discount(self):
        """Покупка одного товара — скидка не применяется"""
        response = self.client.post(reverse('checkout'), {
            'person': 'Анна',
            'address': 'Самара',
            'products': [self.jeans.id]
        })
        
        order = Order.objects.get(person='Анна')
        self.assertEqual(order.total_price, 2000)