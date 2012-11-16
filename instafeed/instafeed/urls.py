from django.conf.urls import patterns, include, url
from emailusernames.forms import EmailUserCreationForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mainapp.views.index', name='index'),
    url(r'^signup/', 'mainapp.views.signup', name='signup'),
    url(r'^signin/', 'mainapp.views.signin', name='signin'),
    url(r'^feed/', 'mainapp.views.feed', name='feed'),
    url(r'^accounts/','mainapp.views.accounts', name='accounts'),
    url(r'^twitter_request/', 'mainapp.views.twitter_request', name='twitter_request'),
    url(r'^facebook_request/', 'mainapp.facebook_views.facebook_request', name='fb_request'),
    url(r'^twitter_signin/', 'mainapp.views.twitter_signin', name='twitter_signin'),
    url(r'^facebook_signin/', 'mainapp.facebook_views.facebook_signin', name='facebook_signin'),
    url(r'^facebook_callback', 'mainapp.facebook_views.facebook_callback', name='facebook_callback'),
    url(r'^facebook_access', 'mainapp.facebook_views.facebook_access', name='facebook_access'),
    url(r'^twitter_callback', 'mainapp.views.twitter_callback', name='twitter_callback'),
    url(r'^faq', 'mainapp.views.faq_request', name='faq_request'),
#    url(r'^google_signup/', 'mainapp.google_views.google_signup', name='google_signup'),
#    url(r'^google_callback_token', 'mainapp.google_views.google_callback_token', name='google_callback_token'),                   
    # url(r'^instafeed/', include('instafeed.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
