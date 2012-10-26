import logging

from datetime import datetime, timedelta

from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache

from .exceptions import RateLimitException

logger = logging.getLogger('ratelimitbackend')


class RateLimitMixin(object):
    """
    A mixin to enable rate-limiting in an existing authentication backend.
    """
    cache_prefix = 'ratelimitbackend-'
    minutes = 5
    requests = 30

    def authenticate(self, username=None, password=None, request=None):
        if request is not None:
            counts = self.get_counters(request)
            if sum(counts.values()) >= self.requests:
                logger.warning(
                    u"Login rate-limit reached: username '{0}', IP {1}".format(
                        username, request.META['REMOTE_ADDR']
                    )
                )
                raise RateLimitException('Rate-limit reached', counts)
        else:
            logger.warning(u"No request passed to the backend, unable to "
                           u"rate-limit. Username was '%s'" % username)
        user = super(RateLimitMixin, self).authenticate(username, password)
        if user is None and request is not None:
            logger.info(
                u"Login failed: username '{0}', IP {1}".format(
                    username,
                    request.META['REMOTE_ADDR'],
                )
            )
            cache_key = self.get_cache_key(request)
            self.cache_incr(cache_key)
        return user

    def get_counters(self, request):
        return cache.get_many(self.keys_to_check(request))

    def keys_to_check(self, request):
        now = datetime.now()
        return [
            self.key(
                request,
                now - timedelta(minutes=minute),
            ) for minute in range(self.minutes + 1)
        ]

    def get_cache_key(self, request):
        return self.key(request, datetime.now())

    def key(self, request, dt):
        return '%s%s-%s' % (
            self.cache_prefix,
            request.META.get('REMOTE_ADDR', ''),
            dt.strftime('%Y%m%d%H%M'),
        )

    def cache_incr(self, key):
        """
        Non-atomic cache increment operation. Not optimal but
        consistent across different cache backends.
        """
        cache.set(key, cache.get(key, 0) + 1, self.expire_after())

    def expire_after(self):
        """Cache expiry delay"""
        return (self.minutes + 1) * 60


class RateLimitModelBackend(RateLimitMixin, ModelBackend):
    pass
