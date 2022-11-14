from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase, Discount

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

def discount_update(purchase_object):
    discount_row = Discount.objects.get(person=purchase_object.person)
    print(purchase_object.id)
    price = Product.objects.get(id=purchase_object.product.id).price
    total = discount_row.total + price
    discount_value = total/10000.0
    Discount.objects.filter(person=purchase_object.person).update(total=total,discount=discount_value)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        discount_update(self.object)
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')


class DiscountCreate(CreateView):
    model = Discount
    fields = ['person', 'total', 'discount']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f'Вы зарегистрированы в программе лояльности, {self.object.person}!')

