#!/usr/bin/env python
import logging
import os
import sys

from django.conf import settings
try:
    from django.utils.functional import empty
except ImportError:
    empty = None


class NullHandler(logging.Handler):  # NullHandler isn't in Python 2.6
    def emit(self, record):
        pass


def setup_test_environment():
    # reset settings
    settings._wrapped = empty

    apps = [
        'django.contrib.sessions',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.messages',
        'ratelimitbackend',
        'tests',
    ]

    middleware_classes = [
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'ratelimitbackend.middleware.RateLimitMiddleware',
    ]

    settings_dict = {
        "DATABASES": {
            'default': {
                'ENGINE': "django.db.backends.sqlite3",
                'NAME': 'ratelimitbackend.sqlite',
            },
        },
        "CACHES": {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            },
        },
        "ROOT_URLCONF": "tests.urls",
        "MIDDLEWARE_CLASSES": middleware_classes,
        "INSTALLED_APPS": apps,
        "SITE_ID": 1,
        "AUTHENTICATION_BACKENDS": (
            'ratelimitbackend.backends.RateLimitModelBackend',
        ),
        "LOGGING": {
            'version': 1,
            'handlers': {
                'null': {
                    'class': 'runtests.NullHandler',
                }
            },
            'loggers': {
                'ratelimitbackend': {
                    'handlers': ['null'],
                },
            },
        },
        "TEMPLATES": [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {
                'loaders': (
                    'django.template.loaders.app_directories.Loader',
                ),
                'context_processors': (
                    'django.contrib.auth.context_processors.auth',
                ),
            },
        }],
    }

    # set up settings for running tests for all apps
    settings.configure(**settings_dict)
    try:
        from django import setup
    except ImportError:
        pass
    else:
        setup()  # Needed for Django>=1.7


def runtests():
    setup_test_environment()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)
    try:
        from django.test.runner import DiscoverRunner
    except ImportError:
        from discover_runner.runner import DiscoverRunner

    runner = DiscoverRunner(verbosity=1, interactive=True, failfast=False)
    failures = runner.run_tests(())
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
