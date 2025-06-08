from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    rating = models.FloatField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat Session {self.session_id} - {self.user.username}"

class ChatMessage(models.Model):
    MESSAGE_TYPES = (
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System'),
    )

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    # For bot responses that include product recommendations
    related_products = models.ManyToManyField(Product, blank=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.session_key}"