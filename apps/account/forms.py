import string
from django.core.validators import RegexValidator
from django import forms
from django.forms import ValidationError
from .models import User, Addresses


FIELD_CLASS = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": FIELD_CLASS,
                "placeholder": "Your email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": FIELD_CLASS,
                "placeholder": "Your password",
            }
        )
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": FIELD_CLASS,
                "placeholder": "Enter email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": FIELD_CLASS,
                "placeholder": "Enter password",
            }
        )
    )


class ProfileForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": " ",
                "readonly": "",
            }
        )
    )

    phone_regex = RegexValidator(regex=r"^\d{11}$", message="Enter valid phone number.")
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=12,
        help_text="example: 09123456789",
        widget=forms.TextInput(attrs={"placeholder": " "}),
    )

    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": " "}))

    birthdate = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "id": "default-datepicker",
                "datepicker": "",
                "placeholder": "Birthday date",
            },
            format="%m/%d/%Y",
        ),
        input_formats=["%m/%d/%Y"],
    )

    class Meta:
        model = User
        fields = ("email", "full_name", "birthdate", "phone_number")


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password1"]
        confirm_password = cleaned_data["password2"]
        if not password and not confirm_password:
            raise ValidationError("you must fill password and confirm password.")
        if password != confirm_password:
            raise ValidationError("password and confirm password not match.")
        
        if len(password) < 6:
            raise ValidationError("Password Must be longer.")

from django import forms

class RequestResetPasswordForm(forms.Form):
    email = forms.EmailField()


class SetPasswordForm(ChangePasswordForm):
    token = forms.CharField(widget=forms.HiddenInput())
    uidb64 = forms.CharField(widget=forms.HiddenInput())

class AddressForm(forms.ModelForm):

    phone_regex = RegexValidator(regex=r"^\d{11}$", message="Enter valid phone number.")
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=12,
        help_text="example: 09123456789",
    )

    class Meta:
        model = Addresses
        fields = (
            "title",
            "province",
            "city",
            "postal_address",
            "phone_number",
            "zipcode",
        )
