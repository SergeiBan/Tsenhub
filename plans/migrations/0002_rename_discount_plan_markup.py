# Generated by Django 4.1.7 on 2023-05-01 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='discount',
            new_name='markup',
        ),
    ]
