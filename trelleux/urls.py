from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('djangosite.trelleux.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^start/$', 'get_started', name='get_started'),
    url(r'^trello_auth/$', 'trello_auth', name='trello_auth'),
)
