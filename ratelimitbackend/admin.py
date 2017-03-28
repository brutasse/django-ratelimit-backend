# Allow transitive imports, e.g.
# `from ratelimitbackend import admin; admin.ModelAdmin`
from django.contrib.admin import *  # noqa
from django.contrib.admin import site as django_site
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import ugettext as _

from .forms import AdminAuthenticationForm
from .views import login


class RateLimitAdminSite(AdminSite):  # noqa
    def login(self, request, extra_context=None):
        """
        Displays the login form for the given HttpRequest.
        """
        context = {
            'title': _('Log in'),
            'app_path': request.get_full_path(),
        }
        if (REDIRECT_FIELD_NAME not in request.GET and
                REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = request.get_full_path()
        context.update(extra_context or {})
        defaults = {
            'extra_context': context,
            'current_app': self.name,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        return login(request, **defaults)


site = RateLimitAdminSite()

for model, admin in django_site._registry.items():
    site.register(model, admin.__class__)
