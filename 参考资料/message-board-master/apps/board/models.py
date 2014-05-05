from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BoardForum(models.Model):
	forum_id = models.AutoField(primary_key=True)
	forum_parent = models.ForeignKey('BoardForum', null=True, blank=True)
	forum_name = models.CharField(max_length=50)
	forum_last_post = models.ForeignKey('BoardPost', null=True, blank=True)
	forum_topic_count = models.IntegerField(default=0)
	forum_post_count = models.IntegerField(default=0)

	def __str__(self):
		return self.forum_name


class BoardTopic(models.Model):
	topic_id = models.AutoField(primary_key=True)
	topic_forum = models.ForeignKey(BoardForum, null=True, blank=True)
	topic_creator = models.ForeignKey(User)
	topic_created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
	topic_name = models.CharField(max_length = 50)
	topic_pinned = models.BooleanField(default=False)
	topic_pinned_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	topic_last_post = models.ForeignKey('BoardPost', null=True, blank=True)
	topic_reply_count = models.IntegerField(default=0)
	topic_view_count = models.IntegerField(default=0)

	def __str__(self):
		return self.topic_name

class BoardPost(models.Model):
	post_id = models.AutoField(primary_key=True)
	post_topic = models.ForeignKey(BoardTopic)
	post_creator = models.ForeignKey(User)
	post_created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
	post_edited_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, default=None)
	post_content = models.TextField(max_length=2000)

	def __str__(self):
		return str(self.post_topic) + " " + str(self.post_id)
