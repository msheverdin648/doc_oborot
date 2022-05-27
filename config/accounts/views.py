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
        if not request.user.is_authenticated and request.user.status:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        users = CustomUser.objects.all()

        context = {
            'users_list': users,
        }
        return render(request, 'personal.html', context)


class PersonalDeleteView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.user.status:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user = CustomUser.objects.get(id=kwargs.get('user_id'))
        user.delete()
        return HttpResponseRedirect('/accounts/personal_edit/')


class PersonalEditView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.user.status:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user = CustomUser.objects.get(id=kwargs.get('user_id'))
        form = EditCustomUserForm(instance=user)
        context = {
            'edit_user': user,
            'form': form
        }
        return render(request, 'personal_edit.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.user.status:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        form = EditCustomUserForm(request.POST or None)
        if form.is_valid():
            personal = CustomUser.objects.get(id=kwargs.get('user_id'))
            personal.first_name = form.cleaned_data['first_name']
            personal.last_name = form.cleaned_data['last_name']
            personal.phone = form.cleaned_data['phone']
            personal.user_group = form.cleaned_data['user_group']
            personal.birthday = form.cleaned_data['birthday']
            personal.status = form.cleaned_data['status']
            personal.personal_post = form.cleaned_data['personal_post']
            personal.percent = form.cleaned_data['percent']
            personal.fixed_pay = form.cleaned_data['fixed_pay']
            personal.save()
            return HttpResponseRedirect(f'/accounts/personal_list/')
        messages.error(request, form.errors)
        return HttpResponseRedirect(f'/accounts/personal_edit/{kwargs.get("user_id")}/')


class SearchPersonal(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.user.status:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        users = CustomUser.objects.none()
        users = CustomUser.objects.filter(last_name=request.GET['q'])
        context = {
            'users_list': users,
        }
        return render(request, 'finance.html', context)


class HomeView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return render(request, 'index.html', {})
