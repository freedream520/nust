from django.contrib import admin

from board.models import BoardForum, BoardTopic, BoardPost

# Register your models here.
admin.site.register(BoardForum)
admin.site.register(BoardTopic)
admin.site.register(BoardPost)