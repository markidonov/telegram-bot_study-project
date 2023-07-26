from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django import forms
from django.contrib.auth.models import User
from .models import Order

command_validator = RegexValidator(r'^[\_a-zA-Z]+$', 'validation')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommandForm(forms.ModelForm):
    command = forms.CharField(label='команда для бота',
        required=True, validators=[command_validator])
    
    class Meta:
        model = Order
        fields = ['command', 'answer']
        