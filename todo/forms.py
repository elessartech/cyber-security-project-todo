from django import forms
from .models import Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TodoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Todo
        fields = ['title', 'details']
        
    def save(self, creator, commit=True):
        instance = super().save(commit=False)
        instance.creator = creator
        if commit:
            instance.save()
        return instance


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
