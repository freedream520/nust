from django.conf.urls import patterns, include, url
from userprofile import views

urlpatterns = patterns('',
	url(r'^profile/$', views.user_profile),
	url(r'^profile/(?P<user_id>\d+)/$', views.show_profile),
)