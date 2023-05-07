from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from email.header import Header
from django.conf import settings

User = get_user_model()


@shared_task
def notify_supplier(seeker_entity, seeker_email):
    h = Header('Назначьте тариф новому пользователю', charset='utf-8')
    send_mail(
        subject=h,
        message=(f'Зарегистрировался пользователь {seeker_entity} с почтой {seeker_email}'),
        from_email=settings.FROM_EMAIL,
        recipient_list=['s.o.banshchikov@yandex.ru']
    )

