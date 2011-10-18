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
