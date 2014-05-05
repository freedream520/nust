from django.conf.urls import patterns, url

from board import views


urlpatterns = patterns('',
    url(r'^/?$', views.board_forum),
    #url(r'^(?P<forum>[a-zA-Z0-9-_]+)/?$', views.board_forum),
    #url(r'^(?P<forum>[a-zA-Z0-9-_]+)/page/(?P<page>[0-9]+)/?$', views.board_forum),
    #url(r'^(?P<forum>[a-zA-Z0-9-_]+)/post/(?P<topic>[0-9]+)/?$', views.board_topic),
    #url(r'^(?P<forum>[a-zA-Z0-9-_]+)/post/(?P<topic>[0-9]+)(?:/(?P<page>[0-9]+))/?$', views.board_topic),
    url(r'^(?P<forum>[0-9]+)/?$', views.board_forum),
    url(r'^page/(?P<page>[0-9]+)/?$', views.board_forum),
    url(r'^(?P<forum>[0-9]+)page/(?P<page>[0-9]+)/?$', views.board_forum),
    url(r'^topic/(?P<topic>[0-9]+)/?$', views.board_topic),
    url(r'^topic/(?P<topic>[0-9]+)(?:/(?P<page>[0-9]+))/?$', views.board_topic),
    url(r'^post/(?P<post>[0-9]+)/?$', views.board_post),
    url(r'^post/(?P<post>[0-9]+)/edit/?$', views.board_post_edit),
    url(r'^topic/(?P<topic>[0-9]+)/addpost/?$', views.board_add_post_ajax),
    url(r'^topic/(?P<topic>[0-9]+)/pin/?$', views.board_pin_topic_ajax),
)