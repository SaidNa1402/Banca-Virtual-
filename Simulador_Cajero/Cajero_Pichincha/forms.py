# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Account

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'identification', 'phone_number', 'password1', 'password2']
        error_messages = {
            'username': {
                'unique': 'Este nombre de usuario ya está en uso.',
                'required': 'El nombre de usuario es obligatorio.'
            },
            'email': {
                'unique': 'Este correo ya está registrado.',
                'invalid': 'Por favor ingrese un correo válido.',
                'required': 'El correo electrónico es obligatorio.'
            },
            'identification': {
                'unique': 'Esta cédula ya está registrada.',
                'invalid': 'Ingrese una cédula válida de 10 dígitos.',
                'required': 'La cédula es obligatoria.'
            },
            'phone_number': {
                'invalid': 'Ingrese un número de teléfono válido de 10 dígitos.',
                'required': 'El número de teléfono es obligatorio.'
            },
            'password1': {
                'invalid': 'Ingrese una contraseña válida.',
                'required': 'La contraseña es obligatoria.',
                'min_length': 'La contraseña debe tener al menos 8 caracteres.',
            },
            'password2': {
                'invalid': 'Ingrese una contraseña válida.',
                'required': 'Debe confirmar su contraseña.',
                'password_mismatch': 'Las contraseñas no coinciden.'
            }
        }
                

class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type']
        labels = {
            'account_type': 'Tipo de cuenta',
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        error_messages={
            'required': 'Por favor ingrese su nombre de usuario.',
            'invalid': 'Usuario inválido.'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        error_messages={
            'required': 'Por favor ingrese su contraseña.',
            'invalid': 'Contraseña inválida.'
        }
    )

    error_messages = {
        'invalid_login': 'Usuario o contraseña incorrectos. Por favor intente nuevamente.',
        'inactive': 'Esta cuenta está inactiva.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['password'].label = 'Contraseña'