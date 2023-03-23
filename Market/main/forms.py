from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields =('email', 'fio', 'phone')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'fio', 'email', 'phone')


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1')


class MakeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ()


class MakeProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'link', 'comment')


class MakeStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('name', 'reason')