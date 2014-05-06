from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webnust.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^polls/', include('polls.urls', namespace="polls")),
	url(r'^account/', include('account.urls', namespace="account")),
	url(r'^t/', include('chat.urls', namespace="chat")),
)
