from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from .models import Passenger
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PassengerForm(ModelForm):
    class Meta:
        model = Passenger
        fields = ('name', 'email', 'phone',)

        labels = {
            'name': _('Passenger name')
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control mb-2',
                    'placeholder': 'enter your name'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control mb-2',
                    'placeholder': 'enter your email'
                }
            ),
            'phone': forms.NumberInput(
                attrs={
                    'class': 'form-control mb-2',
                    'placeholder': 'enter your phone'
                }
            )
        }
