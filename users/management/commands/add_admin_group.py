from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from parts.models import Part


new_group, created = Group.objects.get_or_create(name='Админы')
ct = ContentType.objects.get_for_model(part)
# Дописать !