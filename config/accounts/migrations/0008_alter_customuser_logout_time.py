# Generated by Django 3.2.6 on 2022-03-24 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_timemanage_logout_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='logout_time',
            field=models.DateTimeField(blank=True, verbose_name='Время выхода пользователя'),
        ),
    ]
