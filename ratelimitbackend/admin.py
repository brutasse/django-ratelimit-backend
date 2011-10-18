from django.contrib.admin import *
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import ugettext as _

from .forms import AdminAuthenticationForm
from .views import login


class RateLimitAdminSite(AdminSite):
    def login(self, request, extra_context=None):
        """
        Displays the login form for the given HttpRequest.
        """
        context = {
            'title': _('Log in'),
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        }
        context.update(extra_context or {})
        defaults = {
            'extra_context': context,
            'current_app': self.name,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        return login(request, **defaults)
site = RateLimitAdminSite()
