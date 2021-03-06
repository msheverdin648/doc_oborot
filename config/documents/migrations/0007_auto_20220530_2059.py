# Generated by Django 3.2.6 on 2022-05-30 17:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20220530_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentmodel',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='В архиве'),
        ),
        migrations.AlterField(
            model_name='documentmodel',
            name='ending_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 30, 20, 59, 26, 687867), null=True, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='documentmodel',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Название документа'),
        ),
    ]
