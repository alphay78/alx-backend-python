from django.contrib import admin
from .models import Message, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "content", "edited", "timestamp")
    search_fields = ("content", "sender__username", "receiver__username")


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "old_content", "edited_at")
    search_fields = ("old_content", "message__content")
