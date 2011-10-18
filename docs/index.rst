Django-ratelimit-backend
========================

Django-ratelimit-backend is an app that allows rate-limiting of login attempts
at the authentication backend level. Login attempts are stored in the cache so
you need a properly configured cache setup.

By default, it blocks any IP that has more than 30 failed login attempts in
the past 5 minutes. The IP can still browse your site, only login attempts are
blocked.

.. toctree::
   :maxdepth: 2

   quickstart
   reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

