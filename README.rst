Django-ratelimit-backend
------------------------

.. image:: https://api.travis-ci.org/brutasse/django-ratelimit-backend.png
   :alt: Build Status
   :target: https://travis-ci.org/brutasse/django-ratelimit-backend

Rate-limit your login attempts at the authentication backend level. Login
attempts are stored in the cache for 5 minutes and IPs with more than 30
failed login attempts in the last 5 minutes are blocked.

The numbers (30 attempts, 5 minutes) as well as the blocking strategy can be
customized.

* Authors: Bruno Renié and `contributors`_

  .. _contributors: https://github.com/brutasse/django-ratelimit-backend/contributors

* Licence: BSD

* Compatibility: Django 1.8 and greater

* Documentation: https://django-ratelimit-backend.readthedocs.io

* Code: https://github.com/brutasse/django-ratelimit-backend

Credits
-------

* Simon Willison for his `ratelimitcache`_ idea

  .. _ratelimitcache: http://blog.simonwillison.net/post/57956846132/ratelimitcache

Hacking
-------

::

    git clone https://brutasse@github.com/brutasse/django-ratelimit-backend.git

Hack and run the tests::

    python setup.py test

To run the tests for all supported Python and Django versions::

    pip install tox
    tox
