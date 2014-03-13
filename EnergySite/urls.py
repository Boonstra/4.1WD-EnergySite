from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
from rest_framework import routers
from measurements import views as measurement_views
from flickr_images import views as flickr_images_views

admin.autodiscover()

api_router = routers.SimpleRouter()
api_router.register(r'^measurements', measurement_views.MeasurementViewSet)
api_router.register(r'^flickr-images', flickr_images_views.ImagesViewSet)

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^devices/', include('devices.urls')),
    url(r'^facilities/', include('facilities.urls')),
    url(r'^measurements/', include('measurements.urls')),

    url(r'^api/', include(api_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', 'facilities.views.process_oauth2_login'),
)