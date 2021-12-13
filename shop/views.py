from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required

from .models import Product, User


@login_required
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


@login_required
def buy(request, product_id):
    product = Product.objects.get(id=product_id)
    user = User.objects.get_or_create(id=request.user.id)[0]
    user.sum = user.sum + product.price
    user.save()
    return HttpResponse(f'Спасибо за покупку, {request.user}! Ваша текущая скидка {user.discount}%')
