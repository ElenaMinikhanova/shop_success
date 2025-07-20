from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']
        labels = {
            'username': 'Логин',
            'email': 'Электронная почта',
            'phone_number': 'Номер телефона',
        }