from django.db import models
from core.views import parse_pricelist
from datetime import datetime


class Part(models.Model):
    name = models.CharField(max_length=256)
    uid = models.CharField(max_length=64)
    initial_price = models.PositiveIntegerField()

    def get_parts(pricelist):
        pricelist = parse_pricelist(pricelist)
        return pricelist
