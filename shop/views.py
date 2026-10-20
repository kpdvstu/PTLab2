from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Product, Order, Purchase

#Оригинальная главная страница
def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

# Оригинальное представление для одного товара 
class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']
    success_url = '/'

# Покупка со скидкой
def checkout(request):
    if request.method == 'POST':
        person = request.POST.get('person')
        address = request.POST.get('address')
        product_ids = request.POST.getlist('products')

        if not product_ids:
            return HttpResponse("Корзина пуста")

        order = Order.objects.create(person=person, address=address)
        total_price = 0
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            Purchase.objects.create(order=order, product=product)
            total_price += product.price

        # ЛОГИКА СКИДКИ (Вариант 10)
        unique_categories = set(products.values_list('category', flat=True))
        
        if len(unique_categories) > 1:
            total_price = int(total_price * 0.9)

        order.total_price = total_price
        order.save()

        return HttpResponse(f"Заказ оформлен! Итоговая сумма: {total_price} руб.")

    products = Product.objects.all()
    return render(request, 'shop/checkout.html', {'products': products})