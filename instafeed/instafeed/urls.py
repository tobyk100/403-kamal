from django.conf.urls import patterns, include, url
from emailusernames.forms import EmailUserCreationForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mainapp.views.index', name='index'),
    url(r'^signup/', 'mainapp.views.signup', name='signup'),
    url(r'^feed/', 'mainapp.views.feed', name='feed'),
    url(r'^accounts/','mainapp.views.accounts', name='accounts'),
    url(r'^feed/twitter_request/', 'mainapp.views.twitter_request', name='twitter_request'),
    url(r'^facebook_request/', 'mainapp.views.facebook_request', name='fb_request'),
    # url(r'^instafeed/', include('instafeed.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
