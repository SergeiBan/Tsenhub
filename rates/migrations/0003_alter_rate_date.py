# Generated by Django 4.1.7 on 2023-05-06 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0002_alter_rate_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
