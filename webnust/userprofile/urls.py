from django.conf.urls import patterns, include, url
from userprofile import views

urlpatterns = patterns('',
	url(r'^profile/$', views.user_profile),
)