from typing import Any

from django.core.management.base import BaseCommand

from users.models import Plan


class Command(BaseCommand):
    help = 'Adds zero discount plan which is the default one for new users'

    def handle(self, *args: Any, **options: Any) -> str | None:
        Plan.objects.create(name='Тариф без скидки', discount=0.0)
        self.stdout.write('Создан нулевой тариф')
