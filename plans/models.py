from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Plan(models.Model):
    markup = models.SmallIntegerField(
        'Размер наценки в процентах',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        unique=True
    )
    name = models.CharField('Название тарифа', max_length=32)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self) -> str:
        return f'{self.markup} {self.name}'
