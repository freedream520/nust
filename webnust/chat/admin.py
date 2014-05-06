from django.contrib import admin
from chat.models import Article


class ChatAdmin(admin.ModelAdmin):
	list_display = ('title', 'body', 'likes','pub_date')
	fieldsets = [
		(None, {'fields': ['title']}),
		('Date information', {'fields': ['body'], 'classes': ['collapse']}),
		(None, {'fields':['likes']}),
		(None, {'fields':['pub_date']}),
	]
	list_filter = ['body']
	search_fields = ['title']

admin.site.register(Article, ChatAdmin)
