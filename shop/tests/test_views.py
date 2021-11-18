from datetime import datetime, timedelta
from django.test import TestCase, Client
from shop.models import Product
import re

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Один или два продука для тестирования Web части
        Product.objects.create(name="book", price="740")
        Product.objects.create(name="pencil", price="300")
        self.datetime = datetime.now()

    def test_shop_purchase(self):
        # Идем на начало сайта
        response = self.client.get('/')
        # Проверяем что страница продуктов доступна
        self.assertEqual(response.status_code, 200)
        # Убедимся, что книга есть в списке на странице
        self.assertContains(response, "book")
        # Находим ссылки на все продукты (google помог)
        self.urls = re.findall('/buy/(?:[-\w.]|(?:%[\da-fA-F]{2}))+', response.content.decode())
        # Идем на первый из продуктов
        response = self.client.get(self.urls[0]+'/')
        # Проверяем, что страница покупки доступна
        self.assertEqual(response.status_code, 200)
        # Проверяем наличе нового поле на форме
        self.assertContains(response, "birthday")

        # Постим данные вчерашнего числа. Нельзя использовать фиксированную дату в прошлом, так как она раз в год может быть днем рождения
        yesterday = datetime.now() - timedelta(days=1)
        # Возьмем id продукта из url путем удаления всего, кроме цифр
        product = re.sub("[^\d]", "", self.urls[0])
        # Покупаем продукт, делаем post на нашу форму с нашими данными
        response = self.client.post(self.urls[0]+'/', data={ 'product': product, 'person' : 'Ivanov Yesterday Birthday', 'address' : 'Svetlaya St.', 'birthday' : yesterday.strftime("%Y-%m-%d")})
        # Поскольку используем redirect во view, 
        # проверяем, что успешный ответ от сервера 302, что форма заказа найдена
        self.assertEqual(response.status_code, 302)
        # Переходим на страницу просмотра заказа, делаем redirect
        response = self.client.get(response.url)
        # Проверяем, что успешный ответ от сервера 200, что форма получена
        self.assertEqual(response.status_code, 200)
        # Проверяем, что нет скидки 
        self.assertFalse("дарим Вам скидку" in response.content.decode())
        # Но есть правильный ответ о покупке
        self.assertTrue("Спасибо за покупку" in response.content.decode())

        # Постим данные сегодняшего числа
        response = self.client.post(self.urls[0]+'/', data={ 'product': product, 'person' : 'Ivanov Today Birthday', 'address' : 'Svetlaya St.', 'birthday' : datetime.now().strftime("%Y-%m-%d")})
        # Проверяем, что успешный ответ от сервера 302, что форма заказа найдена
        self.assertEqual(response.status_code, 302)
        # Переходим на страницу просмотра заказа
        response = self.client.get(response.url)
        # Проверяем, что успешный ответ от сервера 200, что форма получена
        self.assertEqual(response.status_code, 200)
        # Проверяем, что показали скидку. Сумму скидки не проверяем, так как за нее отвечает модель
        self.assertTrue("дарим Вам скидку" in response.content.decode())
       
    # Проверим, что страница выполненых заказов просто доступна     
    # Для проверки данных на этой форме, тест нужно выполнять внутри test_shop_purchase 
    def test_shop_orders(self):
        response = self.client.get('/orders')
        # Проверяем, что успешный ответ от сервера 200, что форма получена
        self.assertEqual(response.status_code, 200)
