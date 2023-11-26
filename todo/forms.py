from django import forms
from .models import Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TodoForm(forms.ModelForm):
    def __init__(self, *args, creator=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = creator
    #   self.fields['creator'].queryset = User.objects.filter(pk=creator.pk)

    class Meta:
        model = Todo
        fields = "__all__"
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.creator = self.creator
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
