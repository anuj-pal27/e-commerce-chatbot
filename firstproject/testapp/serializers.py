from rest_framework import serializers
from .models import Product, ChatSession, ChatMessage, UserSession
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid login credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            data['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ChatSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'session_id', 'created_at', 'updated_at', 'is_active', 'message_count']

    def get_message_count(self, obj):
        return obj.messages.count()

class ChatMessageSerializer(serializers.ModelSerializer):
    related_products = ProductSerializer(many=True, read_only=True)
    timestamp_formatted = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'message_type', 'content', 'timestamp', 'timestamp_formatted', 'related_products']

    def get_timestamp_formatted(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')

class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['content']

class ProductSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=50, required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_rating = serializers.FloatField(required=False)
    in_stock_only = serializers.BooleanField(default=True)