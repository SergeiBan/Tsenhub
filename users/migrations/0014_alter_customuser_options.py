# Generated by Django 4.1.7 on 2023-04-29 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_customuser_plan_delete_plan'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('-date_joined',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]