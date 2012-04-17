from django.conf.urls.defaults import patterns, include, url
from lesphonefinder.settings import STATIC_PREFIX
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
                           url(r'^$', 'lesphonefinder.views.home'),
                           url(r'^update/$', 'lesphonefinder.views.update'),
                           url(r'^logout/$', 'lesphonefinder.views.logout_view'),
                           url(r'^reg_mobile/$', 'lesphonefinder.accounts.views.register_mobile'),
                           url(r'^view_map/(?P<mobile_id>\d+)/$', 'lesphonefinder.views.view_mobile_map'),
    # url(r'^$', 'lesphonefinder.views.home', name='home'),
    # url(r'^lesphonefinder/', include('lesphonefinder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
