from django.conf.urls import patterns, url
from notification import views

urlpatterns = patterns('',
	url(r'^show/(?P<notification_id>\d+)/$', views.show_notification),
	url(r'^delete/(?P<notification_id>\d+)/$', views.delete_notification),

)