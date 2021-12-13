from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    @property
    def discount(self):
        if self.sum < 1000:
            discount_value = 0
        elif self.sum < 10000:
            discount_value = 2
        elif self.sum < 100000:
            discount_value = 5
        elif self.sum < 1000000:
            discount_value = 10
        else:
            discount_value = 25

        return discount_value
