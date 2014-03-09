from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
from rest_framework import viewsets, routers
from measurements import views

admin.autodiscover()

api_router = routers.DefaultRouter()
api_router.register(r'^measurements', views.MeasurementViewSet)

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^devices/', include('devices.urls')),
    url(r'^facilities/', include('facilities.urls')),
    url(r'^measurements/', include('measurements.urls')),

    url(r'^api/', include(api_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)