# Generated by Django 3.2.6 on 2022-05-30 17:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0005_auto_20220530_0918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentmodel',
            name='author',
        ),
        migrations.RemoveField(
            model_name='documentmodel',
            name='change_date',
        ),
        migrations.RemoveField(
            model_name='documentmodel',
            name='doc_from',
        ),
        migrations.RemoveField(
            model_name='documentmodel',
            name='private',
        ),
        migrations.RemoveField(
            model_name='documentmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='ending_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 30, 20, 32, 51, 491580), null=True, verbose_name='Дата окончания'),
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='status',
            field=models.CharField(choices=[('added', 'Создан'), ('waiting', 'Ожидает'), ('terminated', 'Расторгнут'), ('submited', 'Подписан'), ('executed', 'Исполнен')], default='added', max_length=255, verbose_name='Статус документа'),
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='user_from',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_from', to=settings.AUTH_USER_MODEL, verbose_name='От кого'),
        ),
        migrations.AddField(
            model_name='documentmodel',
            name='user_to',
            field=models.ManyToManyField(null=True, related_name='user_to', to=settings.AUTH_USER_MODEL, verbose_name='Кому'),
        ),
        migrations.AlterField(
            model_name='documentmodel',
            name='description',
            field=models.TextField(null=True, verbose_name='Краткое содержание документа'),
        ),
        migrations.AlterField(
            model_name='documentmodel',
            name='file',
            field=models.FileField(null=True, upload_to='documents/', verbose_name='Электронный файл докуента'),
        ),
        migrations.AlterField(
            model_name='documentmodel',
            name='theme',
            field=models.CharField(max_length=255, null=True, verbose_name='Вид документа'),
        ),
    ]
