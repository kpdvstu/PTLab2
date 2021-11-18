from django.db import models
from datetime import date, datetime

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    # день рождения - часть покупки
    birthday = models.DateField(default=None, blank=True, null=True)
    # скидка - часть покупки - может быть не только по поводу дня рождения
    discount = models.DecimalField(max_digits=3, decimal_places = 0, default = 0)
    sale_amount = models.DecimalField(max_digits=30, decimal_places = 2, default = 0)
    date = models.DateTimeField(auto_now_add=True)
