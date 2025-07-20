from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль',
        error_messages={
            'required': 'Пожалуйста, введите пароль.',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']
        labels = {
            'username': 'Логин',
            'email': 'Электронная почта',
            'phone_number': 'Номер телефона',
        }
        error_messages = {
            'username': {
                'required': 'Пожалуйста, введите логин.',
            },
            'email': {
                'required': 'Пожалуйста, введите электронную почту.',
                'invalid': 'Введите корректный адрес электронной почты.',
            },
            'phone_number': {
                'required': 'Пожалуйста, введите номер телефона.',
            },
        }