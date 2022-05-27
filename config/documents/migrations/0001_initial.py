# Generated by Django 3.2.6 on 2022-05-20 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=255, verbose_name='Номер договора')),
                ('name', models.CharField(max_length=255, verbose_name='Название договора')),
                ('file', models.FileField(upload_to='documents/', verbose_name='Электронный файл договора')),
            ],
            options={
                'verbose_name': 'Документ',
            },
        ),
    ]