Usage
=====

Installation
------------

::

    pip install django-ratelimit-backend

There's nothing to add to your ``INSTALLED_APPS``, unless you want to run the
tests. In which case, add ``'ratelimitbackend'``.

Quickstart
----------

* Set your ``AUTHENTICATION_BACKENDS`` to:

  .. code-block:: python

      AUTHENTICATION_BACKENDS = (
          'ratelimitbackend.backends.RateLimitModelBackend',
      )

  If you have a custom backend, see the :ref:`backends reference <backends>`.

* Everytime you use ``django.contrib.auth.views.login``, use
  ``ratelimitbackend.views.login`` instead.

* Whenever you use ``django.contrib.admin``, use ``ratelimitbackend.admin``
  instead.

  In your ``urls.py``:

  .. code-block:: python

      from ratelimitbackend import admin

      admin.autodiscover()

      urlpatterns += patterns('',
          (r'^admin/', include(admin.site.urls)),
      )

  In your apps' ``admin.py`` files:

  .. code-block:: python

      from ratelimitbackend import admin

      from .models import SomeModel

      admin.site.register(SomeModel)

* Add ``'ratelimitbackend.middleware.RateLimitMiddleware'`` to your
  ``MIDDLEWARE_CLASSES``, or create you own middleware to handle rate limits.
  See the :ref:`middleware reference <middleware>`.

* If you use ``django.contrib.auth.forms.AuthenticationForm`` directly,
  replace it with ``ratelimitbackend.forms.AuthenticationForm`` and **always**
  pass it the request object. For instance:

  .. code-block:: python

      if request.method == 'POST':
          form = AuthenticationForm(data=request.POST, request=request)
          # etc. etc.

Customizing rate-limiting criteria
----------------------------------

By default, rate limits are based on the IP of the client. An IP that submits
a form too many times gets rate-limited, whatever it submits. For custom
rate-limiting you can subclass the backend and implement your own logic.

Let's see with an example: instead of checking the client's IP, we will use a
combination of the IP *and* the tried username. This way after 30 failed
attempts with one username, people can start brute-forcing a new username.
Yay! More seriously, it can become useful if you have lots of users logging in
at the same time from the same IP.

While we're at it, we'll also allow 50 login attempts every 10 minutes.

To do this, simply subclass
``ratelimitbackend.backends.RateLimitModelBackend``:

.. code-block:: python

    from ratelimitbackend.backends import RateLimitModelBackend

    class MyBackend(RateLimitModelBackend):
        minutes = 10
        requests = 50

        def key(self, request, dt):
            return '%s%s-%s-%s' % (
                self.cache_prefix,
                request.META.get('REMOTE_ADDR', ''),
                request.POST['username'],
                dt.strftime('%Y%m%d%H%M'),
            )

The ``key()`` method is used to build the cache keys storing the login
attempts. The default implementation doesn't use POST data, here we're adding
another part to the cache key.

Note that we're not sanitizing anything, so we may end up with a rather long
cache key. Be careful.

For all the details about the rate-limiting implementation, see the
:ref:`backend reference <backends>`.

Using with other backends
-------------------------

.. _custom_backends:

The way django-ratelimit-backend is implemented requires the authentication
backends to have an ``authenticate()`` method with 3 arguments (``username``,
``password``, ``request``) instead of only two.

While django-ratelimit-backend works fine with the default ``ModelBackend`` by
providing a replacement class, it's obviously not possible to do that for every
single backend.

The way to deal with this is to create a custom class using the
``RateLimitMixin`` class before registering the backend in your settings. For
instance, for the LdapAuthBackend::

    from django_auth_ldap.backend import LDAPBackend
    from ratelimitbackend.backends import RateLimitMixin

    class RateLimitedLDAPBackend(RateLimitMixin, LDAPBackend):
        pass

    AUTHENTICATION_BACKENDS = (
        'path.to.settings.RateLimitedLDAPBackend',
    )

``RateLimitMixin`` lets you simply add rate-limiting capabilities to any
authentication backend.
