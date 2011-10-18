from django import forms
from django.contrib.admin.forms import (
    AdminAuthenticationForm as AdminAuthForm, ERROR_MESSAGE,
)
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm as AuthForm
from django.contrib.auth.models import User
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
                      'Note that both fields are case-sensitive.'),
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_('This account is inactive.'))
        self.check_for_test_cookie()
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
                if u'@' in username:
                    # Mistakenly entered e-mail address instead of username?
                    # Look it up.
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = _(
                                "Your e-mail address is not your username."
                                " Try '%s' instead.") % user.username
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise forms.ValidationError(message)
        self.check_for_test_cookie()
        return self.cleaned_data
