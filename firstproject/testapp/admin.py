from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product, ChatSession, ChatMessage, UserSession

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'rating']
    list_filter = ['category']
    search_fields = ['name', 'description']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'session_id']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content Preview"

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'created_at', 'last_activity']
    list_filter = ['created_at', 'last_activity']
    search_fields = ['user__username']

# User model is already registered by default in Django admin
