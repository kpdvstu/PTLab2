from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=100, default='Общее') 

    def __str__(self):
        return self.name

class Order(models.Model):
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField(default=0) # итоговая сумма со скидкой

    def __str__(self):
        return f"Заказ от {self.person} ({self.date})"

class Purchase(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)