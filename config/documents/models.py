from django.db import models

from accounts.models import CustomUser


class DocumentModel(models.Model):
    number = models.IntegerField('Номер договора')
    name = models.CharField('Название договора', max_length=255)
    type = models.CharField('Тип документа', max_length=255, null=True)
    author = models.CharField('Автор документа', max_length=255, null=True)
    doc_from = models.CharField('Отдел откуда документ', max_length=255, null=True)
    description = models.TextField('Краткое описание документа', null=True)
    theme = models.CharField('Тема документа', max_length=255, null=True)
    user = models.ForeignKey(CustomUser, verbose_name='Кто добавил', on_delete=models.CASCADE, null=True)
    load_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    change_date = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    file = models.FileField(verbose_name='Электронный файл договора', upload_to='documents/')

    def __str__(self):
        return f'{self.name} номер: {self.number}'

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
