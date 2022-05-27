from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class RegisterCustomUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'user_group', 'status', 'is_staff')


class EditCustomUserForm(ModelForm):
    class Meta(ModelForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'user_group', 'status')


class LoginUserForm(ModelForm):
    class Meta(ModelForm):
        model = CustomUser
        fields = ('username', 'password')
