from django.conf.urls import patterns, include, url
from django.contrib import admin

import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'message-board.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^/?$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^board/', include('board.urls')),
)
