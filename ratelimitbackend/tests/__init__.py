#-*- coding: utf-8 -*-
import warnings

import django

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.unittest import skipIf

try:
    from django.contrib.auth import get_user_model
except ImportError:
    pass


class RateLimitTests(TestCase):
    urls = 'ratelimitbackend.tests.urls'

    def setUp(self):
        cache.clear()

    def assertRateLimited(self, response):
        self.assertContains(response, 'Too many failed login attempts',
                            status_code=403)

    @override_settings(AUTH_USER_MODEL='tests.User')
    @skipIf(django.VERSION[:2] < (1, 5), "Swappable user not available")
    def test_ratelimit_login_attempt_swapped_user(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')

        wrong_data = {
            'username': u'hï',
            'password': 'suspicious attempt',
        }
        # 30 failing attempts are allowed
        for iteration in range(30):
            response = self.client.post(url, wrong_data)
            self.assertContains(response, 'username')

        response = self.client.post(url, wrong_data)
        self.assertRateLimited(response)

        # IP is rate-limited; even valid login attempts are blocked.
        get_user_model().objects.create_user('foo@bar.com', 'pass')
        response = self.client.post(url, {'username': 'foo',
                                          'password': 'pass'})
        self.assertRateLimited(response)

    def test_ratelimit_login_attempt(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')

        wrong_data = {
            'username': u'hï',
            'password': 'suspicious attempt',
        }
        # 30 failing attempts are allowed
        for iteration in range(30):
            response = self.client.post(url, wrong_data)
            self.assertContains(response, 'username')

        response = self.client.post(url, wrong_data)
        self.assertRateLimited(response)

        # IP is rate-limited; even valid login attempts are blocked.
        User.objects.create_user('foo', 'foo@bar.com', 'pass')
        response = self.client.post(url, {'username': 'foo',
                                          'password': 'pass'})
        self.assertRateLimited(response)

    @override_settings(AUTH_USER_MODEL='tests.User')
    @skipIf(django.VERSION[:2] < (1, 5), "Swappable user not available")
    def test_ratelimit_login_attempt_swapped(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')

        wrong_data = {
            'username': u'hï',
            'password': 'suspicious attempt',
        }
        # 30 failing attempts are allowed
        for iteration in range(30):
            response = self.client.post(url, wrong_data)
            self.assertContains(response, 'username')

        response = self.client.post(url, wrong_data)
        self.assertRateLimited(response)

        # IP is rate-limited; even valid login attempts are blocked.
        get_user_model().objects.create_user('foo@bar.com', 'pass')
        response = self.client.post(url, {'username': 'foo',
                                          'password': 'pass'})
        self.assertRateLimited(response)

    def test_ratelimit_admin_logins(self):
        url = reverse('admin:index')
        response = self.client.get(url, follow=True)
        login_url = response.request['PATH_INFO']
        self.assertContains(response, 'username')
        wrong_data = {
            'username': u'hî',
            'password': 'suspicious attempt',
        }
        # 30 failing attempts are allowed
        for iteration in range(30):
            response = self.client.post(login_url, wrong_data)
            self.assertContains(response, 'username')
            self.assertContains(response, 'for a staff account')

        response = self.client.post(login_url, wrong_data)
        self.assertRateLimited(response)

    def test_django_registry(self):
        user = User.objects.create_user('username', 'foo@bar.com', 'pass')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        with warnings.catch_warnings(record=True) as w:
            self.client.login(request=None, username='username',
                              password='pass')
            self.assertEqual(len(w), 1)
        url = reverse('admin:index')
        response = self.client.get(url)
        self.assertContains(response, 'in the Auth')
        self.assertContains(response, '"/admin/auth/user/add/"')

    def test_custom_ratelimit_logic(self):
        """Custom backend behaviour"""
        url = reverse('login')
        old_backends = settings.AUTHENTICATION_BACKENDS
        settings.AUTHENTICATION_BACKENDS = (
            'ratelimitbackend.tests.backends.TestBackend',
        )

        wrong_data = {
            'username': u'ùser1',
            'password': 'suspicious attempt',
        }
        # 50 failing attempts are allowed
        for iteration in range(50):
            response = self.client.post(url, wrong_data)
            self.assertContains(response, 'username')

        # Attempts for this username are blocked
        response = self.client.post(url, wrong_data)
        self.assertRateLimited(response)

        # Further attempts with another username are allowed
        wrong_data['username'] = 'user2'
        response = self.client.post(url, wrong_data)
        self.assertContains(response, 'username')

        settings.AUTHENTICATION_BACKENDS = old_backends

    @override_settings(AUTHENTICATION_BACKENDS=(
        'ratelimitbackend.tests.backends.TestCustomBackend',))
    def test_custom_backend(self):
        """Backend with custom authentication method"""
        url = reverse('custom_login')
        response = self.client.get(url)
        self.assertContains(response, 'token')
        self.assertContains(response, 'secret')

        wrong_data = {
            'token': u'hï',
            'secret': 'suspicious attempt',
        }
        # 30 failed attempts are allowed
        for iteration in range(30):
            response = self.client.post(url, wrong_data)
        self.assertContains(response, 'secret')

        response = self.client.post(url, wrong_data)
        self.assertRateLimited(response)

        # IP is rate-limited; even valid login attempts are blocked.
        User.objects.create_user('foo', 'foo@bar.com', 'pass')
        response = self.client.post(url, {'token': 'foo',
                                          'secret': 'pass'})
        self.assertRateLimited(response)

    @override_settings(AUTHENTICATION_BACKENDS=(
        'ratelimitbackend.tests.backends.TestCustomBrokenBackend',))
    def test_custom_backend_no_username_key(self):
        """Custom backend with missing username_key"""
        url = reverse('custom_login')
        wrong_data = {
            'token': u'hï',
            'secret': 'suspicious attempt',
        }
        self.assertRaises(KeyError, self.client.post, url, wrong_data)
