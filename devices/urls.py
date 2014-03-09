from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EnergySite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'devices.views.index', name='index'),
    url(r'^add/', 'devices.views.add', name='add'),
    url(r'^view/', 'devices.views.view', name='view'),
)
