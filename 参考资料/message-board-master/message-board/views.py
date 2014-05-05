from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import redirect, render

from board.models import BoardForum, BoardTopic, BoardPost

def index(request):
	return render(request, 'index.html', 
		{
			'forum_count': BoardForum.objects.aggregate(Count('forum_id'))['forum_id__count'],
			'topic_count': BoardTopic.objects.aggregate(Count('topic_id'))['topic_id__count'],
			'post_count': BoardPost.objects.aggregate(Count('post_id'))['post_id__count']
		})