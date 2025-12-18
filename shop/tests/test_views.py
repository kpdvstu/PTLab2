from django.test import TestCase, Client
from django.contrib.auth.models import User
from ..models import Product, CartItem


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='password')
        self.product = Product.objects.create(
            title="Виски",
            price=2500,
            description="Крепкий"
        )

    def test_homepage(self):
        """Проверяем, что главная страница открывается"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Виски")  # Товар должен быть на странице

    def test_add_to_cart_authenticated(self):
        """Проверяем добавление в корзину (для авторизованного)"""
        self.client.login(username='tester', password='password')

        # Эмулируем клик "В корзину"
        response = self.client.get(f'/add/{self.product.id}/', follow=True)
        self.assertEqual(response.status_code, 200)

        # Проверяем базу данных
        item = CartItem.objects.get(user=self.user, product=self.product)
        self.assertEqual(item.quantity, 1)

    def test_cart_page(self):
        """Проверяем, что страница корзины открывается"""
        self.client.login(username='tester', password='password')
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)