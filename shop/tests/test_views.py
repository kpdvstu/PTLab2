from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase

class PurchasePriceIncreaseTestCase(TestCase):
    def setUp(self):
        # Инициализация клиента для тестирования и создание тестового продукта.
        self.client = Client()
        self.product = Product.objects.create(name="chair", price=100, total_sold=0)
        # Получение URL для тестовых покупок.
        self.purchase_url = reverse('buy', args=[self.product.id])
        
    def create_purchase(self, quantity):
        # Функция для создания тестовых покупок.
        return self.client.post(self.purchase_url, {
            'product': self.product.id, 
            'person': 'Test Person',
            'address': 'Test Address',
            'quantity': quantity
        })
    
    def test_purchase_increase_total_sold(self):
        # Проверка, что после покупки увеличивается количество проданных единиц.
        self.create_purchase(1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.total_sold, 1)

    def test_price_increase_every_ten_purchases(self):
        # Проверка, что после каждой 10-й покупки происходит увеличение цены.
        self.create_purchase(9)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 100)  # цена не должна измениться
        
        self.create_purchase(1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 125)  # цена должна увеличиться на 25%

    def test_multiple_purchases_increase_price_correctly(self):
        # Проверка, что двойное увеличение цены происходит корректно при достижении пороговых значений продаж.
        self.create_purchase(20)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 156)  # цена должна увеличиться дважды
    
    def test_purchase_redirect_or_render_correct_template(self):
        # Проверка, что после покупки происходит использование нужного шаблона (или перенаправление, если это требуется).
        response = self.create_purchase(1)
        self.assertTemplateUsed(response, 'shop/byesuccses.html')
        # ИЛИ если вы ожидаете перенаправление, можно использовать следующее:
        # self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, ...)

