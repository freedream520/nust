from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from chat import views

urlpatterns = patterns('',
	#url(r'^$', views.IndexView.as_view(), name='index'),
	#url(r'^vote/$', views.vote, name='vote'),
	url(r'^all/$', views.articles),
	url(r'^(?P<article_id>\d+)/$', views.article,),
	#url(r'^language/(?P<language>[a-z\-]+)/$', 'article.views.language'),
	url(r'^create/$', views.create),
	url(r'^like/(?P<article_id>\d+)/$', views.like_article),
	#url(r'^add_comment/(?P<article_id>\d+)/$', 'article.views.add_comment'),
	#url(r'^delete_comment/(?P<comment_id>\d+)/$', 'article.views.delete_comment'),
	url(r'^search/$', views.search_titles),
)

if settings.DEBUG:
	urlpatterns += staticfiles_urlpatterns()