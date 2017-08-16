from django.forms import Form, ValidationError, CharField, PasswordInput
from django.contrib.auth import authenticate


class CustomAuthForm(Form):
    token = CharField(max_length=30)
    secret = CharField(widget=PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(CustomAuthForm, self).__init__(*args, **kwargs)

    def clean(self):
        token = self.cleaned_data.get('token')
        secret = self.cleaned_data.get('secret')
        if token and secret:
            self.user_cache = authenticate(token=token,
                                           secret=secret,
                                           request=self.request)
            if self.user_cache is None:
                raise ValidationError("Invalid")
            elif not self.user_cache.is_active:
                raise ValidationError("Inactive")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class TokenOnlyAuthForm(Form):
    token = CharField(max_length=30)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(TokenOnlyAuthForm, self).__init__(*args, **kwargs)

    def clean_token(self):
        token = self.cleaned_data.get('token')

        # This is NOT how a token-only authentication system should work, but
        # it allows us to simulate one for testing relatively easily.
        username, password = token.split('_')
        self.user_cache = authenticate(username=username,
                                       password=password,
                                       request=self.request)
        if self.user_cache is None:
            raise ValidationError("Invalid")
        elif not self.user_cache.is_active:
            raise ValidationError("Inactive")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
