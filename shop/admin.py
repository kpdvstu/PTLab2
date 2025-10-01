# Register your models here.

from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "sold_count", "initial_quantity")
    search_fields = ("name",)
    list_filter = ("price", "quantity")
    ordering = ("-sold_count",)  # сортировка по количеству проданных

