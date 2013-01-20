from django.http import HttpResponseForbidden

from .exceptions import RateLimitException


class RateLimitMiddleware(object):
    """
    Handles exceptions thrown by rate-limited login attepmts.
    """
    def process_exception(self, request, exception):
        if isinstance(exception, RateLimitException):
            return HttpResponseForbidden(
                'Too many failed login attempts. Try again later.',
                content_type='text/plain',
            )
