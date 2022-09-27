from django.contrib import admin
from .models import *
from chat.models import ChatMessage, Friend


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email']
admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'updated']
admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'created', 'updated']
    list_editable = ['text']
admin.site.register(Comment, CommentAdmin)


admin.site.register([Friend, Subscriber, Topic, ChatMessage, Like])