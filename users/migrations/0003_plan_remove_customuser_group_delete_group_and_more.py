# Generated by Django 4.1.7 on 2023-04-16 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_group_customuser_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField(verbose_name='Размер скидки в процентах')),
                ('name', models.CharField(max_length=32, verbose_name='Название тарифа')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
            },
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='group',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.AddField(
            model_name='customuser',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='users.plan'),
        ),
    ]
