Reference
---------

.. _backends:

Authentication backends
```````````````````````

.. module:: ratelimitbackend.backends
   :synopsis: Backend classes for enabling rate-limiting.

.. class:: RateLimitMixin

    This is where the rate-limiting logic is implemented. Failed login
    attempts are cached for 5 minutes and when the treshold is reached, the
    remote IP is blocked whether its attempts are valid or not.

.. attribute:: RateLimitMixin.cache_prefix

    The prefix to use for cache keys. Defaults to ``'ratelimitbackend-'``

.. attribute:: RateLimitMixin.minutes

    Number of minutes after which login attempts are not taken into account.
    Defaults to ``5``.

.. attribute:: RateLimitMixin.requests

    Number of login attempts to allow during ``minutes``. Defaults to ``30``.

.. method:: RateLimitMixin.authenticate(username, password, request)

    Tries to ``authenticate(username, password)`` on the parent backend and
    use the request for rate-limiting.

.. method:: RateLimitMixin.get_counters(request)

    Fetches the previous failed login attempts from the cache. There is one
    cache key per minute slot.

.. method:: RateLimitMixin.keys_to_check(request)

    Returns the list of keys to try to fetch from the cache for previous login
    attempts. For a 5-minute limit, this returns the 5 relevant cache keys.

.. method:: RateLimitMixin.get_cache_key(request)

    Returns the cache key for the current time. This is the key to increment
    if the login attempt has failed.

.. method:: RateLimitMixin.key(request, dt)

    Derives a cache key from the request and a datetime object. The datetime
    object can be present (for the current request) or past (for the previous
    cache keys).

.. method:: RateLimitMixin.cache_incr(key)

    Performs an increment operation on ``key``. The implementation is **not**
    atomic. If you have a cache backend that supports atomic increment
    operations, you're advised to override this method.

.. method:: RateLimitMixin.expire_after()

    Returns the cache timeout for keys.

.. class:: RateLimitModelBackend

    A rate-limited version of ``django.contrib.auth.backends.ModelBackend``.

    This is a subclass of ``django.contrib.auth.backends.ModelBackend`` that
    adds rate-limiting. If you have custom backends, make sure they inherit
    from this instead of the default ``ModelBackend``.

    If your backend has nothing to do with Django’s auth system, use
    ``RateLimitMixin`` to inject the rate-limiting functionality in your
    backend.

Exceptions
``````````

.. module:: ratelimitbackend.exceptions
   :synopsis: Exceptions thrown when the limit is reached.

.. class:: RateLimitException

    The exception thrown when a user reaches the limits.

.. attribute:: RateLimitException.counts

    A dictionnary containing the cache keys for every minute and the
    corresponding failed login attempts.

    Example:

    .. code-block:: python

        {
            'ratelimitbackend-127.0.0.1-201110181448': 12,
            'ratelimitbackend-127.0.0.1-201110181449': 18,
        }

Admin
`````

.. module:: ratelimitbackend.admin
   :synopsis: The admin site with rate limits.

.. class:: RateLimitAdminSite

    Rate-limited version of the default Django admin site. If you use the
    default admin site (``django.contrib.admin.site``), it won’t be
    rate-limited.

    If you have a custom admin site (inheriting from ``AdminSite``), you need to
    make it inherit from ``ratelimitbackend.RateLimitAdminSite``, replacing:

    .. code-block:: python

        from django.contrib import admin

        class AdminSite(admin.AdminSite):
            pass
        site = AdminSite()

    with:

    .. code-block:: python

        from ratelimitbackend import admin

        class AdminSite(admin.RateLimitAdminSite):
            pass
        site = AdminSite()

    Make sure your calls to ``admin.site.register`` reference the correct admin
    site.

.. method:: RateLimitAdminSite.login(request, extra_context=None)

    This method calls django-ratelimit-backend's version of the login view.

.. _middleware:

Middleware
``````````

.. module:: ratelimitbackend.middleware

.. class:: RateLimitMiddleware

    This middleware catches ``RateLimitException`` and returns a 403 instead,
    with a ``'text/plain'`` mimetype. Use your custom middleware if you need a
    different behaviour.

Views
`````

.. module:: ratelimitbackend.views

.. function:: login(request[, template_name, redirect_field_name, authentication_form])

    This function uses a custom authentication form and passes it the request
    object. The external API is the same as `Django's login view`_.

    .. _Django's login view: https://docs.djangoproject.com/en/dev/topics/auth/#django.contrib.auth.views.login

Forms
`````

.. module:: ratelimitbackend.forms

.. class:: AuthenticationForm

    A subclass of `Django's authentication form`_ that passes the request
    object to the ``authenticate()`` function, hence to the authentication
    backend.

    .. _Django's authentication form: https://docs.djangoproject.com/en/dev/topics/auth/#django.contrib.auth.forms.AuthenticationForm

Logging
```````

Failed attempts are logged using a logger named ``'ratelimitbackend'``. Here
is an example for logging to the standard output:

.. code-block:: python

    LOGGING = {
        'formatters': {
            'simple': {
                'format': '%(asctime)s %(levelname)s: %(message)s'
            },
            # other formatters
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            # other handlers
        },
        'loggers': {
            'ratelimitbackend': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            # other loggers
        },
    }

You will see two kinds of messages:

* "No request passed to the backend, unable to rate-limit. Username was…"

  This means you're not using the app correctly, the request object wasn't
  passed to the authentication backend. Double-check the documentation, and if
  you make manual calls to login-related functions you may need to pass the
  request object manually.

  The log level for this message is: ``WARNING``.

* "Login failed: username 'foo', IP 127.0.0.1"

  This is a failed attempt that has been temporarily cached.

  The log level for this message is: ``INFO``.

* "Login rate-limit reached: username 'foo', IP 127.0.0.1"

  This means someone has used all his quotas and got a
  ``RateLimitException``, locking him temporarily until the quota decreases.

  The log level for this message is: ``WARNING``.
