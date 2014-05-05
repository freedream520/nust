from django.conf.urls import patterns, url

from users import views


urlpatterns = patterns('',
    url(r'^/?$', views.users_index, name='index'),
    url(r'^signup/?$', views.users_signup, name='signup'),
    url(r'^login/?$', views.users_login, name='login'),
    url(r'^profile/?$', views.users_profile, name='profile'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/?$', views.users_profile, name='profile'),
    url(r'^welcome/?$', views.users_welcome, name='welcome'),
    url(r'^logout/?$', views.users_logout, name='logout'),
)