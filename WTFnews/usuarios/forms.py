from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class SingUpForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Username'), 'autofocus': True}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Email')}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}))

    def clean_name(self):
        name = self.cleaned_data['name']
        if User.objects.filter(username=self.cleaned_data['name']).exists():
            raise forms.ValidationError(_('This username is already being used.'))
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_('This email is already being used.'))
        return email


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("Invalid Email and/or password."),
    }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()

    def confirm_login_allowed(self, user):
        pass


class ChangePasswordForm(PasswordChangeForm):
    error_messages = {
        'password_mismatch': _("The new password is not the same as the password confirmation."),
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autofocus': True, 'placeholder': _('Old password')}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('New password')}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirm new password')}))
