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

    # Password reset
    url(r'^reset/', 'django.contrib.auth.views.password_reset'),
    url(r'^password_reset_done/', 'django.contrib.auth.views.password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', \
        'django.contrib.auth.views.password_reset_confirm'), \
    url(r'^password_reset_complete/', 'django.contrib.auth.views.password_reset_complete'), \

    # Password change
    url(r'^password_change/', 'django.contrib.auth.views.password_change'), \
    url(r'^password_change_done/', 'django.contrib.auth.views.password_change_done'), \

    url(r'^feed/', 'mainapp.views.feed', name='feed'),
    url(r'^twitter_request/', 'mainapp.twitter_views.twitter_request', name='twitter_request'),
    url(r'^facebook_request/', 'mainapp.facebook_views.facebook_request', name='fb_request'),
    url(r'^twitter_signin/', 'mainapp.twitter_views.twitter_signin', name='twitter_signin'),
    url(r'^facebook_signin/', 'mainapp.facebook_views.facebook_signin', name='facebook_signin'),
    url(r'^facebook_callback', 'mainapp.facebook_views.facebook_callback', name='facebook_callback'),
    url(r'^facebook_access', 'mainapp.facebook_views.facebook_access', name='facebook_access'),
    url(r'^twitter_callback', 'mainapp.twitter_views.twitter_callback', name='twitter_callback'),
    url(r'^faq', 'mainapp.views.faq_request', name='faq_request'),
    url(r'^settings', 'mainapp.views.settings', name="settings"),
    url(r'^logout', 'mainapp.views.logoutuser', name='logout'),
#    url(r'^google_signup/', 'mainapp.google_views.google_signup', name='google_signup'),
#    url(r'^google_callback_token', 'mainapp.google_views.google_callback_token', name='google_callback_token'),
    url(r'^twitter_callback', 'mainapp.twitter_views.twitter_callback', name='twitter_callback'),
    url(r'^google_signin/', 'mainapp.google_views.google_signup', name='google_signup'),
    url(r'^google_callback_code', 'mainapp.google_views.google_callback_code', name='google_callback_code'),
    url(r'^google_get_posts', 'mainapp.google_views.google_get_posts', name='google_get_posts'),
    url(r'^scheduled_update', 'mainapp.views.scheduled_update', name='scheduled_update'),
    url(r'^delete_scheduled_update', 'mainapp.views.delete_scheduled_update', name='delete_scheduled_update'),
    url(r'^schedule', 'mainapp.views.schedule', name='schedule'),
    # url(r'^instafeed/', include('instafeed.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
