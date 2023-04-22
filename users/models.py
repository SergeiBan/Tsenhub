from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from users.managers import CustomUserManager
from django.core.mail import send_mail
from django.conf import settings


class Plan(models.Model):
    discount = models.FloatField(
        'Размер скидки в процентах',
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        unique=True
    )
    name = models.CharField('Название тарифа', max_length=32)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self) -> str:
        return f'{self.discount} {self.name}'


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
            subject='Подтверждение регистрации на Запчастице',
            message=(
                f'Для активации вашей учетной записи необходимо перейти по '
                f'ссылке: {settings.THIS_HOST}/verify-user/?token={token}'
            ),
            from_email=settings.FROM_EMAIL,
            recipient_list=[email]
        )
