from django.core.validators import RegexValidator
from django import forms
from .models import User


FIELD_CLASS = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class":FIELD_CLASS,
        "placeholder":"Your email",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":FIELD_CLASS,
        "placeholder":"Your password",
    }))

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class":FIELD_CLASS,
            "placeholder":"Enter email",
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":FIELD_CLASS,
        "placeholder":"Enter password",
    }))

class ProfileForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\d{11}$',
        message="Enter valid phone number."
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': ' ',
            'readonly':"",
        }))
    
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=12,
        help_text="مثال: 123-456-7890",
        widget=forms.TextInput(attrs={
            'placeholder': ' '
        })
    )
    
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': ' '
        })
    )
    
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'text',
            'id': 'default-datepicker',
            "datepicker":"",
            'placeholder': 'Birthday date'
        },format='%m/%d/%Y'
        ),
        input_formats=['%m/%d/%Y']
    )

    class Meta:
        model = User
        fields = ("email" ,"full_name" ,"birthdate" ,"phone_number")
