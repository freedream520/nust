from django.conf.urls import patterns, url
from account import views
from account.forms import ContactForm1, ContactForm2, ContactForm3
from account.views import ContactWizard
urlpatterns = patterns('',
	url(r'^register/$', views.register_user, name='register'),
	url(r'^register_success/$', views.register_success, name='register_success'),
	url(r'^login/$', views.login, name='login'),
	url(r'^auth', views.auth_view, name='auth'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^loggedin/$', views.loggedin, name='loggedin'),
	url(r'^invalid/$', views.invalid_login, name='invalid'),
	url(r'^contact/$', ContactWizard.as_view([ContactForm1, ContactForm2, ContactForm3])),
)


