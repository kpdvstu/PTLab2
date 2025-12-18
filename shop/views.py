from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem


def index(request):
    # Эта функция у тебя уже есть, просто убедись, что она передает товары
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})


@login_required(login_url='/admin/')  # Требуем вход (для лабы можно входить как админ)
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Пытаемся получить товар в корзине у этого юзера
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    # Если товар уже был - увеличиваем количество
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('index')


@login_required(login_url='/admin/')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    # Считаем итого
    total_quantity = sum(item.quantity for item in cart_items)
    total_sum = sum(item.total_price() for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_sum': total_sum
    })