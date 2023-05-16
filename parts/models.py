from django.db import models

from core.views import parse_pricelist


class Part(models.Model):
    uid = models.CharField(max_length=32)
    initial_price = models.DecimalField(max_digits=9, decimal_places=2)

    def get_parts(pricelist):
        return parse_pricelist(pricelist)
