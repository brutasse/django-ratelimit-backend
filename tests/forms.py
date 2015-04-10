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
