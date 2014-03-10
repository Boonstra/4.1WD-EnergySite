from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EnergySite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'facilities.views.index', name='index'),
    url(r'^add/', 'facilities.views.add', name='add'),
    url(r'^view/', 'facilities.views.view', name='view'),
    url(r'^register/', 'facilities.views.register', name='register'),
    url(r'^register_resident/', 'facilities.views.register_resident'),
    url(r'^delete_residents/', 'facilities.views.delete_resident'),
    url(r'^login/', 'facilities.views.login', name='login'),
    url(r'^logout/', 'facilities.views.logout', name='logout'),
)
