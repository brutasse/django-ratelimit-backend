Django-ratelimit-backend
========================

Django-ratelimit-backend is an app that allows rate-limiting of login attempts
at the authentication backend level. Login attempts are stored in the cache so
you need a properly configured cache setup.

By default, it blocks any IP that has more than 30 failed login attempts in
the past 5 minutes. The IP can still browse your site, only login attempts are
blocked.

.. note::

    If you use a custom authentication backend, there is an additional
    configuration step. Check the :ref:`custom backends <custom_backends>`
    section.

.. toctree::
   :maxdepth: 2

   usage
   reference

Get involved, submit issues and pull requests on the `code repository`_!

.. _code repository: https://github.com/brutasse/django-ratelimit-backend

Changes
-------

* **1.1** (TBA):

  * Exclude tests from being installed from the wheel file.

  * Add support for Django 1.10 and 1.11.

* **1.0** (2015-07-10):

  * Silence warnings with Django 1.8.

* **0.6.4** (2015-03-31):

  * Only set the redirect field to the value of ``request.get_full_path()`` if
    the field does not already have a value. Patch by Michael Blatherwick.

* **0.6.3** (2015-02-12):

  * Add ``RatelimitMixin.get_ip``.

* **0.6.2** (2014-07-28):

  * Django 1.7 support. Patch by Mathieu Agopian.

* **0.6.1** (2014-01-21):

  * Removed calls to deprecated ``check_test_cookie()``.

* **0.6** (2013-04-18):

  The ``RatelimitBackend`` now allows arbitrary ``kwargs`` for authentication,
  not just ``username`` and ``password``. Patch by Trey Hunner.

* **0.5** (2013-02-14):

  * Python 3 compatibility.

  * The backend now issues a warning (``warnings.warn()``) instead of a logging
    call when no request is passed to the backend. This is because such cases
    are developer errors so a warning is more appropriate.

* **0.4** (2013-01-20):

  * Automatically re-register models which have been registered in
    Django's default admin site instance. There is no need to register
    3rd-party models anymore.

  * Fixed a couple of deprecation warnings.

* **0.3** (2012-11-22):

  * Removed the part where the admin login form looked up a User object
    when an email was used to login. This brings support for Django 1.5's
    swappable user models.

* **0.2** (2012-07-31):

  * Added a logging call when a user reaches its rate-limit.

* **0.1**:

  * Initial version.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
