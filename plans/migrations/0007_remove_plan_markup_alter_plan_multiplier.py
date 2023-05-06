# Generated by Django 4.1.7 on 2023-05-06 21:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0006_alter_plan_multiplier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='markup',
        ),
        migrations.AlterField(
            model_name='plan',
            name='multiplier',
            field=models.DecimalField(decimal_places=4, max_digits=9, unique=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Наценка - множитель'),
        ),
    ]
