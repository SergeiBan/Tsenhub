from django.db import models


class Part(models.Model):
    uid = models.CharField(max_length=32)
    initial_price = models.DecimalField(max_digits=9, decimal_places=2)
