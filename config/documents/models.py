from datetime import datetime

from django.db import models

from accounts.models import CustomUser


class DocumentModel(models.Model):
    ADDED = 'added'
    WAITING = 'waiting'
    TERMINATED = 'terminated'
    EXECUTED = 'executed'
    READ = 'read'
    SUBMITED = 'submited'

    DOCUMENT_ACTION = [
        (READ, 'Ознакомление'),
        (SUBMITED, 'Подпись'),
    ]

    DOCUMENT_STATUSES = [
        (ADDED, 'Создан'),
        (WAITING, 'Ожидает'),
        (READ, 'Ознакомлен'),
        (TERMINATED, 'Расторгнут'),
        (SUBMITED, 'Подписан'),
        (EXECUTED, 'Исполнен')
    ]
    name = models.CharField('Название документа', max_length=255, null=True)
    theme = models.CharField('Вид документа', max_length=255, null=True)
    number = models.IntegerField('Номер договора', null=True)
    type = models.CharField('Тип документа', max_length=255, null=True)
    description = models.TextField('Краткое содержание документа', null=True)
    status = models.CharField('Статус документа', choices=DOCUMENT_STATUSES, max_length=255, default=ADDED)
    action = models.CharField('Отправить на..', choices=DOCUMENT_ACTION, max_length=255, default=READ)

    load_date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    ending_date = models.DateTimeField(verbose_name='Дата окончания', null=True, default=datetime.now())

    submited = models.BooleanField(verbose_name='Подписан', default=False)
    archived = models.BooleanField('В архиве', default=False)
    user_from = models.ForeignKey(CustomUser,
                                  verbose_name='От кого',
                                  on_delete=models.CASCADE,
                                  null=True,
                                  related_name='user_from')
    user_to = models.ForeignKey(CustomUser, verbose_name='Кому', on_delete=models.CASCADE, null=True, related_name='user_to')
    file = models.FileField(verbose_name='Электронный файл докуента', upload_to='documents/', null=True)

    def __str__(self):
        return f'{self.name} номер: {self.number}, статус: {self.status}'

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
