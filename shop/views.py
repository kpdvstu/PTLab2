from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Product, Purchase

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address', 'quantity']
    template_name = 'shop/purchase_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        product = self.object.product
        previous_total_sold = product.total_sold
        
        # Вычисляем, сколько единиц продукта куплено по каждой из цен
        for _ in range(self.object.quantity):
            product.total_sold += 1
            if product.total_sold % 10 == 0:
                product.price *= 1.25  # увеличиваем цену на 25% каждый раз, когда достигается порог в 10 единиц
            product.save()

        # Теперь, когда мы обновили цену и общее количество проданных единиц продукта, можем сохранить покупку
        self.object.save()

        return render(self.request, 'shop/byesuccses.html', {'person': self.object.person})

