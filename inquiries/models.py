from django.db import models
from django.contrib.auth import get_user_model
from parts.models import Part


User = get_user_model()


class Inquiry(models.model):
    seeker = models.ForeignKey(
        User, on_delete=models.CASCDE, related_name='inquiries')
    part = models.ForeignKey(
        Part, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='parts')