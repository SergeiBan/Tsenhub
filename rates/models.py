from django.db import models


class Rate(models.Model):
    currency = models.CharField(max_length=8)
    rate = models.DecimalField(max_digits=8, decimal_places=4)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
