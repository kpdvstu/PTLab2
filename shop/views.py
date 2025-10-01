from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


#class PurchaseCreate(CreateView):
#    model = Purchase
#    fields = ['product', 'person', 'address']
#
#    def form_valid(self, form):
#        self.object = form.save()
#        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')

from django.shortcuts import redirect, get_object_or_404

def buy_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        product.sell(1)  # покупаем 1 штуку
    except ValueError:
        # если товара нет
        return HttpResponse("Товар закончился :(")
    return redirect("index")


