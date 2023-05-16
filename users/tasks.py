from email.header import Header

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


@shared_task
def notify_supplier(seeker_entity, seeker_email):
    h = Header('Назначьте тариф новому пользователю', charset='utf-8')
    send_mail(
        subject=h,
        message=(
            f'Зарегистрировался пользователь {seeker_entity} '
            f'с почтой {seeker_email}'),
        from_email=settings.FROM_EMAIL,
        recipient_list=['alex.kuzmenko84@mail.ru']
    )
