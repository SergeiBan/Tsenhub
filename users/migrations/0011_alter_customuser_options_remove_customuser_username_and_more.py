# Generated by Django 4.1.7 on 2023-04-21 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('-date_joined',)},
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='entity',
            field=models.CharField(default='Hehehe', max_length=128),
            preserve_default=False,
        ),
    ]
