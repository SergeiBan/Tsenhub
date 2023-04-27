from django.db import models

from core.views import parse_pricelist


class Part(models.Model):
    uid = models.CharField(max_length=64)
    initial_price = models.PositiveIntegerField()

    def get_parts(pricelist):
        pricelist = parse_pricelist(pricelist)
        return pricelist
