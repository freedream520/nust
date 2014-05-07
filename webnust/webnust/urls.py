from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django import views
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
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

if settings.DEBUG:
	urlpatterns += staticfiles_urlpatterns()

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)