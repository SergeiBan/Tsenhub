from celery import shared_task
from parts.models import Part


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def count_parts():
    return Part.objects.count()
