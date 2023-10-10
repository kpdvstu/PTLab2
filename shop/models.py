from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    total_sold = models.PositiveIntegerField(default=0)


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
