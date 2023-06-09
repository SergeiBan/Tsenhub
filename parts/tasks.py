from email.header import Header

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage


@shared_task
def send_order(seeker_pk, seeker_entity, seeker_email, seeker_phone_n):
    h = Header('Заказ на Запчастице', charset='utf-8')
    email = EmailMessage(
        subject=h,
        body=(
            f'Заказ\nот пользователя {seeker_entity}\n'
            f'почта {seeker_email}\nтелефон {seeker_phone_n}'
        ),
        from_email=settings.FROM_EMAIL,
        to=['alex.kuzmenko84@mail.ru'],
    )
    email.attach_file(f'last_orders/{seeker_pk}_order.xlsx')
    email.send()
