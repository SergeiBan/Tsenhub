# Generated by Django 4.1.7 on 2023-05-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='amount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]