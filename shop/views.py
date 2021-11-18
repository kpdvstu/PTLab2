from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.views.generic.edit import CreateView
from .models import Product, Purchase
from django.views.generic.edit import FormView
from datetime import date, datetime

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

class PurchaseCreate(CreateView):
    model = Purchase
    # Скидка рассчитывается в зависимости от birthdsay согласно условию
    fields = ['product', 'person', 'address', 'birthday']

    def form_valid(self, form):
        self.object = form.save()
        # Если месяц и день рождения совпадают с текущей датой, значит скидка 10%, иначе нет скидки
        if self.object.birthday.day == datetime.today().day and self.object.birthday.month == datetime.today().month:
            self.object.discount = 10
        else:
            self.object.discount = 0
        self.object.sale_amount = round(float(self.object.product.price) * (1 - self.object.discount/100), 2)
        # Обновим заказ с нужными данными
        self.object = form.save()
        # Если форма валидная, все сохранилось, то считаем, что все хорошо и переходим на order view 
        return redirect(f'/order/{self.object.id}/')

# Форма выполненого заказа, которая знает как трактовать скидку и как вывести заказ
# Также получить информацию о заказе можно через http://localhost:8000/order/id_заказа/
# Чем мы и воспользуемся на форме orders (список выполненых заказов)
# Пример http://localhost:8000/order/1/
def order(request, purchase_id):
    discount_text = ""
    # Находим заказ по первичному ключу purchase_id
    try: 
        purchase = Purchase.objects.get(pk=purchase_id)
    except:
        # Если заказа нет, выводим ошибку
        return HttpResponse(f'Заказ № {purchase_id} не найден!')
    
    # Достаем продукт по id
    product = Product.objects.get(pk=purchase.product.id)
    # Формируем данные для формы выполненного заказа
    context = {'purchase': purchase, 'product' : product} 
    # Трактуем скидку просто по ее наличию (поскольку других скидок нет) 
    if purchase.discount > 0:
        discount_text = f'Поздравляем Вас с Днем рождения и дарим Вам скидку {purchase.discount}%!'
        # Добавлем текст скидки в данные для формы
        context['discount_text'] = discount_text
    # Выводим детали заказа
    return render(request, 'shop/order.html', context)

# Список выполненных заказов
def orders(request):
    # Получаем список
    purchases = Purchase.objects.all()
    context = {'purchases': purchases}
    # Выводим список заказов
    return render(request, 'shop/orders.html', context)
