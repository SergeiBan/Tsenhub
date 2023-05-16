from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Inquiry(models.Model):
    seeker = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='inquiries')
    part = models.CharField(max_length=32)
    amount = models.IntegerField()
    inquiry_date = models.DateTimeField()
    made_into_order = models.BooleanField(default=False)
