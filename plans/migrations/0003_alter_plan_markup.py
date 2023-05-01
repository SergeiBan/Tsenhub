# Generated by Django 4.1.7 on 2023-05-01 11:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0002_rename_discount_plan_markup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='markup',
            field=models.FloatField(unique=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Размер наценки в процентах'),
        ),
    ]
