from django.conf.urls import url

from trelleux import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^start/$', views.get_started, name='get_started'),
    url(r'^trello_auth/$', views.trello_auth, name='trello_auth'),
]
