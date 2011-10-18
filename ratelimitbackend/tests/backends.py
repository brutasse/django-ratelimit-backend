from ..backends import RateLimitModelBackend


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
