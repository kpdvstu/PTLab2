from decimal import Decimal, ROUND_HALF_UP
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    # Новые поля для варианта 8:
    initial_quantity = models.PositiveIntegerField(default=0)  # изначальный остаток 
    sold_count = models.PositiveIntegerField(default=0)        # сколько всего продано

    def _reprice_if_threshold_crossed(self, old_sold: int, new_sold: int):
        """
        После каждой десятой продажи повышаем цену на 15%.
        Если за один вызов sell() мы пересекли несколько «десятков»,
        применим повышение столько раз, сколько порогов пересекли.
        """
        old_blocks = old_sold // 10
        new_blocks = new_sold // 10
        bumps = new_blocks - old_blocks
        if bumps > 0:
            for _ in range(bumps):
                self.price = (Decimal(self.price) * Decimal('1.15')).quantize(
                    Decimal('0.01'),
                    rounding=ROUND_HALF_UP
                )

    def sell(self, pcs: int = 1):
        """
        Совершить покупку pcs штук:
        - уменьшаем остаток,
        - увеличиваем счётчик продаж,
        - повышаем цену на 15% при пересечении 10/20/30... продаж.
        """
        if pcs <= 0:
            raise ValueError("pcs must be positive")
        if self.quantity < pcs:
            raise ValueError("Not enough stock")

        old_sold = self.sold_count
        self.quantity -= pcs
        self.sold_count += pcs

        self._reprice_if_threshold_crossed(old_sold, self.sold_count)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.quantity} pcs)"
