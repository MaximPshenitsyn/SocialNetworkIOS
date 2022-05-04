from django import forms
from django.forms import formset_factory


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Почта (@edu.hse.ru):', max_length=128, required=True)
    password = forms.CharField(label='Пароль:', max_length=128, required=True, widget=forms.PasswordInput)
    username = forms.CharField(label='Имя:', max_length=128, required=True)
    role = forms.ChoiceField(label='Роль:', choices=[('Student', 'student'), ('Assistant', 'assistant'),
                                                     ('Teacher', 'teacher')], required=True)
    picture = forms.FileField(label='Фото профиля:', required=False)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Почта (@edu.hse.ru):', max_length=128, required=True)
    password = forms.CharField(label='Пароль:', max_length=128, required=True, widget=forms.PasswordInput)


class EditUserForm(forms.Form):
    password = forms.CharField(label='Пароль:', max_length=128, required=False, widget=forms.PasswordInput)
    username = forms.CharField(label='Имя:', max_length=128, required=False)
    picture = forms.FileField(label='Фото профиля:', required=False)
