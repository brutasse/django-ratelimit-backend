from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from ..backends import RateLimitMixin, RateLimitModelBackend


class TestBackend(RateLimitModelBackend):
    minutes = 10
    requests = 50

    def key(self, request, dt):
        """Derives the cache key from the submitted username too."""
        return '%s%s-%s-%s' % (
            self.cache_prefix,
            request.META.get('REMOTE_ADDR', ''),
            request.POST['username'],
            dt.strftime('%Y%m%d%H%M'),
        )


class CustomBackend(ModelBackend):
    def authenticate(self, token=None, secret=None):
        try:
            user = User.objects.get(username=token)
            if user.check_password(secret):
                return user
        except User.DoesNotExist:
            return None


class TestCustomBackend(RateLimitMixin, CustomBackend):
    """Rate-limited backend with token/secret instead of username/password"""
    username_key = 'token'


class TestCustomBrokenBackend(RateLimitMixin, CustomBackend):
    """Rate-limited backend with token/secret instead of username/password"""
