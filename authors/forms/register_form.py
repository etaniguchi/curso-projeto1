from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.core.exceptions import ValidationError
from utils.django_forms import add_attr, add_placeholder, strong_password

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Your password'
        }),
        error_messages = {
            'required': 'Password must not be empty'
        },
        help_text = {
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        },
        validators = [strong_password]
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Repeat your password'
        }),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
        ]
        # exclude = ['first_name']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'The e-mail must be valid.'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }
        widget = {
            'first_name': forms.TextInput(attrs={
                    'placeholder':'Type your first name here.',
                    'class':'input text-input'
            }),
            'password': forms.PasswordInput(attrs = {
                    'placeholder': 'Type your password here.'
            })
        }

    def clean_password(self):
        # data = self.data -- sem tratamento dos dados
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(pipoca)s no campo password',
                code='invalid',
                params={'pipoca':'"atenção"'}
            )
        
        return data


    def clean_first_name(self):
        # data = self.data -- sem tratamento dos dados
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value':'"John Doe"'}
            )
        
        return data
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                'User e-mail is already in use',
                code='invalid',
            )
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                    'Password and password2 must be equal',
                    code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                    'Another error',
                ],
            })

