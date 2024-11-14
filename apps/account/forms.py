from django import forms

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