from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext, gettext_lazy as _


class LoginForm(forms.Form):
    username = auth_forms.UsernameField(widget=forms.TextInput(attrs={
        'id': 'mail',
        'type': 'email',
    }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'id': 'pw',
            'type': 'password',
            'autocomplete': 'current_password',
        }),
    )

class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label=_("Name"),
        strip=False,
        widget=forms.TextInput(attrs={
            'id': 'regname',
        }),
    )
    last_name = forms.CharField(
        label=_("Surname"),
        strip=False,
        widget=forms.TextInput(attrs={
            'id': 'regsurname',
        }),
    )
    username = auth_forms.UsernameField(widget=forms.TextInput(attrs={
        'id': 'mail',
        'type': 'email',
    }))
    phone_number = forms.CharField(
        label=_("Telephone number"),
        strip=False,
        widget=forms.NumberInput(attrs={
            'id': 'regphone',
        }),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'id': 'regpw1',
            'type': 'password',
            'autocomplete': 'current_password',
        }),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'id': 'regpw2',
            'type': 'password',
            'autocomplete': 'current_password',
        }),
    )

    def clean(self):
        if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
            self.add_error("password2", "Passwords do not match!")
        elif len(self.cleaned_data.get("password1")) < 8:
            self.add_error("password1", "Password is too short!")
        return self.cleaned_data

class RecoverPasswordForm(forms.Form):
    username = auth_forms.UsernameField(widget=forms.TextInput(attrs={
        'id': 'recmail',
        'type': 'email',
    }))