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

* 0.4: automatically re-register models which have been registered in Django's
  default admin site instance. There is no need to register 3rd-party models
  anymore.

  Fixed a couple of deprecation warnings.

* 0.3: removed the part where the admin login form looked up a User object when
  an email was used to login. This brings support for Django 1.5's swappable
  user models.

* 0.2: added a logging call when a user reaches its rate-limit.

* 0.1: initial version.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

