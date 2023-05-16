from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from email.header import Header
from django.conf import settings


@shared_task
def send_order(seeker_pk, seeker_entity, seeker_email, seeker_phone_n):
    h = Header('Заказ на Запчастице', charset='utf-8')
    email = EmailMessage(
        subject=h,
        message=(
            f'Заказ\nот пользователя {seeker_entity}\n'
            f'почта {seeker_email}\nтелефон {seeker_phone_n}'
        ),
        from_email=settings.FROM_EMAIL,
        to=['alex.kuzmenko84@mail.ru'],
    )
    email.attach_file(f'{seeker_pk}_order.xlsx')
    email.send()
    # send_mail(
    #     subject=h,
    #     message=(
    #         f'Заказ\nот пользователя {seeker_entity}\n'
    #         f'почта {seeker_email}\nтелефон {seeker_phone_n}'
    #     ),
    #     from_email=settings.FROM_EMAIL,
    #     recipient_list=['alex.kuzmenko84@mail.ru']
    # )
