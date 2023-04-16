from django.db import models
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    discount = models.FloatField()
    name = models.CharField(max_length=32)


class CustomUser(AbstractUser):
    group = models.ForeignKey(
        Group, null=True, on_delete=models.CASCADE, related_name='users')
