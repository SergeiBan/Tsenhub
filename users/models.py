from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

from plans.models import Plan
from users.managers import CustomUserManager

ROLE_CHOICES = (
    ('seeker', 'покупатель'),
    ('supplier', 'продавец')
)


class CustomUser(AbstractUser):
    username = None
    entity = models.CharField(max_length=128)
    plan = models.ForeignKey(
        Plan, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='users'
    )
    email = models.EmailField('Почта', unique=True)
    role = models.CharField(
        max_length=32, choices=ROLE_CHOICES, default='seeker')

    objects = CustomUserManager()
    confirmation_token = models.CharField(max_length=32, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['entity']

    class Meta:
        ordering = ('-date_joined',)

    def send_register_confirmation(self, email, token):
        send_mail(
            subject='Registration confirmation',
            message=(
                f'Для активации вашей учетной записи необходимо перейти по\n'
                f'ссылке: {settings.THIS_HOST}/verify-user/?token={token}'
            ),
            from_email=settings.FROM_EMAIL,
            recipient_list=[email]
        )
