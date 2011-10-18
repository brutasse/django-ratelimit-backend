from django.conf.urls.defaults import include, patterns, url

from .. import admin
from ..views import login


urlpatterns = patterns('',
    url(r'^login/$', login,
        {'template_name': 'admin/login.html'}, name='login'),
    url(r'^admin/', include(admin.site.urls)),
)
