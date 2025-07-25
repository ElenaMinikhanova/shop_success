from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
        label='Пароль',
        error_messages={
            'required': '',
        }
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
        error_messages={
            'required': '',
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username': 'Логин',
            'email': 'Электронная почта',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Электронная почта'}),
        }
        error_messages = {
            'username': {
                'required': '',
            },
            'email': {
                'required': '',
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = self.data.get("password_confirm")
        if password != password_confirm:
            self.add_error('password_confirm', "Пароли не совпадают")
        return cleaned_data