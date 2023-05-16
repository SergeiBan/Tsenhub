from celery import shared_task
from parts.models import Part


@shared_task
def save_order(quotes, seeker_pk):
    with open(f'{seeker_pk}_order.xlsx', 'wb+') as destination:
            destination.write(quotes.getbuffer())
