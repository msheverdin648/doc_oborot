from django.contrib.sessions.management.commands import clearsessions
from django.contrib.sessions.models import Session
from .models import CustomUser, TimeManage
from django.utils import  timezone




def scheduled_logout():
  users = CustomUser.objects.all()
  Session.objects.all().delete()
  for user in users:
      user.logout_time = timezone.now()
      user.save()
      time_data = TimeManage.objects.filter(personal=user.pk).last()
      time_data.logout_time = timezone.now()
      time_data.save()