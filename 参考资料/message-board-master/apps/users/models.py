from django.db import models
from django.contrib.auth.models import User


class UserMessage(models.Model):
	user_from = models.ForeignKey(User, related_name='from')
	user_to = models.ForeignKey(User, related_name='to')
	content = models.TextField(max_length=500)
	date = models.DateTimeField(auto_now=False, auto_now_add=True)