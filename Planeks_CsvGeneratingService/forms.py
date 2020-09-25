from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            try:
                db_user = User.objects.get(username=username).username
                db_password = User.objects.get(username=username).password
            except:
                db_user = "User doesn't exist"
                db_password = "Password doesn't exist"
            if username != db_user:
                raise forms.ValidationError('Такого пользователя не существует')
            elif not check_password(password, db_password):
                raise forms.ValidationError('Неверный пароль')

        return super(UserLoginForm, self).clean(*args, **kwargs)
