from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class Plan(models.Model):
    discount = models.FloatField(
        'Размер скидки в процентах',
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        unique=True
    )
    name = models.CharField('Название тарифа', max_length=32)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self) -> str:
        return f'{self.discount} {self.name}'


ROLE_CHOICES = (
    ('seeker', 'покупатель'),
    ('supplier', 'продавец')
)


class CustomUser(AbstractUser):
    plan = models.ForeignKey(
        Plan, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='users'
    )
    email = models.EmailField('Почта', unique=True)
    role = models.CharField(
        max_length=32, choices=ROLE_CHOICES, default='seeker')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
