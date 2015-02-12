from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm as AdminAuthForm

try:
    from django.contrib.admin.forms import ERROR_MESSAGE
except ImportError:
    # The ERROR_MESSAGE has been moved in Django>=1.7
    ERROR_MESSAGE = AdminAuthForm.error_messages['invalid_login']

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm as AuthForm
from django.utils.translation import ugettext_lazy as _


class AuthenticationForm(AuthForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password,
                                           request=self.request)
            if self.user_cache is None:
                raise forms.ValidationError(
                    _('Please enter a correct username and password. '
                      'Note that both fields may be case-sensitive.'),
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_('This account is inactive.'))
        return self.cleaned_data


class AdminAuthenticationForm(AdminAuthForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password,
                                           request=self.request)
            if self.user_cache is None:
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise forms.ValidationError(message)
        return self.cleaned_data
