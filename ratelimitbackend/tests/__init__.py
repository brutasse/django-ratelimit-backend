from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase


class RateLimitTests(TestCase):
    urls = 'ratelimitbackend.tests.urls'

    def setUp(self):
        cache.clear()

    def test_ratelimit_login_attempt(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')

        wrong_data = {
            'username': 'hi',
            'password': 'suspicious attempt',
        }
        # 30 failing attempts are allowed
        for iteration in xrange(30):
            response = self.client.post(url, wrong_data)
            self.assertContains(response, 'username')

        response = self.client.post(url, wrong_data)
        self.assertContains(response, 'Too many failed login attempts',
                            status_code=403)

        # IP is rate-limited; even valid login attempts are blocked.
        User.objects.create_user('foo', 'foo@bar.com', 'pass')
        response = self.client.post(url, {'username': 'foo',
                                          'password': 'pass'})
        self.assertEqual(response.status_code, 403)

    def test_ratelimit_admin_logins(self):
        url = reverse('admin:index')
        response = self.client.get(url)
        self.assertContains(response, 'username')
        wrong_data = {
            'username': 'hi',
            'password': 'suspicious attempt',
        }
        # 30 failing attempts are allowed
        for iteration in xrange(30):
            response = self.client.post(url, wrong_data)
            self.assertContains(response, 'username')

        response = self.client.post(url, wrong_data)
        self.assertContains(response, 'Too many failed login attempts',
                            status_code=403)
