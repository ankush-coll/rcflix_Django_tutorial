from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        email = forms.EmailField(required=True)
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter your username',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Enter password'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Re-enter password'
            }),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        # Remove help text for password fields
            self.fields['password2'].help_text = None