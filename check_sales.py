import os
import django


# Настраиваем Django окружение
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tplab2.settings")
django.setup()

from shop.models import Product

def demo_sales(product_name="Тестовый смартфон"):
    # Создаём товар, если его нет
    p, created = Product.objects.get_or_create(
        name=product_name,
        defaults={
            "price": 20000.00,
            "quantity": 30,
            "initial_quantity": 30,
            "sold_count": 0,
        }
    )

    # Если товар уже был, сбрасываем состояние
    if not created:
        p.price = 20000.00
        p.quantity = 30
        p.initial_quantity = 30
        p.sold_count = 0
        p.save()

    print(f"До продаж: {p.price}, sold_count={p.sold_count}, quantity={p.quantity}")

    # 10 продаж
    for i in range(10):
        p.sell(1)
    p.refresh_from_db()
    print(f"После 10 продаж: {p.price}, sold_count={p.sold_count}, quantity={p.quantity}")

    # ещё 10 продаж
    for i in range(10):
        p.sell(1)
    p.refresh_from_db()
    print(f"После 20 продаж: {p.price}, sold_count={p.sold_count}, quantity={p.quantity}")


if __name__ == "__main__":
    demo_sales()
