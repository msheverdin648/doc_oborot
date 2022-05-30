# accounts/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegisterCustomUserForm, EditCustomUserForm
from .models import CustomUser
from django.views.generic.base import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect


class SignUpView(generic.CreateView):
    form_class = RegisterCustomUserForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class PersonalListView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        users = CustomUser.objects.all()

        context = {
            'users_list': users,
        }
        return render(request, 'personal.html', context)


class PersonalDeleteView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user = CustomUser.objects.get(id=kwargs.get('user_id'))
        user.delete()
        return HttpResponseRedirect('/accounts/personal_edit/')


class SearchPersonal(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        users = CustomUser.objects.none()
        users = CustomUser.objects.filter(last_name=request.GET['q'])
        context = {
            'users_list': users,
        }
        return render(request, 'finance.html', context)

