# Generated by Django 4.1.7 on 2023-05-16 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0003_alter_inquiry_part'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='made_into_order',
            field=models.BooleanField(default=False),
        ),
    ]
