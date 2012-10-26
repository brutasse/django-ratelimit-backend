#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase


class RateLimitTests(TestCase):
    urls = 'ratelimitbackend.tests.urls'

    def setUp(self):
        cache.clear()

    def assertRateLimited(self, response):
        self.assertContains(response, 'Too many failed login attempts',
                            status_code=403)

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
        for iteration in xrange(30):
            response = self.client.post(url, wrong_data)
            self.assertContains(response, 'username')

        response = self.client.post(url, wrong_data)
        self.assertRateLimited(response)

        # IP is rate-limited; even valid login attempts are blocked.
        User.objects.create_user('foo', 'foo@bar.com', 'pass')
        response = self.client.post(url, {'username': 'foo',
                                          'password': 'pass'})
        self.assertRateLimited(response)

    def test_ratelimit_admin_logins(self):
        url = reverse('admin:index')
        response = self.client.get(url)
        self.assertContains(response, 'username')
        wrong_data = {
            'username': u'hî',
            'password': 'suspicious attempt',
        }
        # 30 failing attempts are allowed
        for iteration in xrange(30):
            response = self.client.post(url, wrong_data)
            self.assertContains(response, 'username')

        response = self.client.post(url, wrong_data)
        self.assertRateLimited(response)

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
        for iteration in xrange(50):
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
