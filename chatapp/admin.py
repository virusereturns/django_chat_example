from django.contrib import admin
from .models import Room, ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'created', 'message')
    list_filter = ('room', 'user')
    search_fields = ('message', 'user__username', 'room__name')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'room', 'user', 'message')


admin.site.register(Room)
