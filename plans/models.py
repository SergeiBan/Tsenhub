from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Plan(models.Model):
    multiplier = models.DecimalField(
        'Наценка - множитель', max_digits=9, decimal_places=4,
        validators=[MinValueValidator(0)], unique=True)
    name = models.CharField('Название тарифа', max_length=32)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self) -> str:
        return f'{self.multiplier} {self.name}'
