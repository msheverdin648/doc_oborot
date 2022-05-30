from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    DIRECTOR = 'director'
    WORKER = 'worker'

    USER_GROUPS = [
        (DIRECTOR, 'Директор'),
        (WORKER, 'Работник'),
    ]

    phone = models.CharField(("Номер телефона"), max_length=14, blank=True)
    email = models.CharField(("Почта"), max_length=255, blank=True)
    user_group = models.CharField(("Группа пользователей"), max_length=255, choices=USER_GROUPS, blank=True, null=True)

