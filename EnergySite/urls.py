from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
import measurements

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EnergySite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^facilities/', include('facilities.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^measurements/', include('measurements.urls')),
)
