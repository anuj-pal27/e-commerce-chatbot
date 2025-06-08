from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.utils import timezone
import uuid

from .models import Product, ChatSession, ChatMessage, UserSession
from .serializers import (
    ProductSerializer, 
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    ChatSessionSerializer,
    ChatMessageSerializer,
    ChatMessageCreateSerializer,
    ProductSearchSerializer
)
from .chatbot_service import ChatbotService

def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        if User.objects.filter(username=data['username']).exists():
            return HttpResponse(json.dumps({'error': 'Username already exists'}), status=400)
        
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        login(request, user)
        return JsonResponse({'message': 'User created successfully'}, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)
        

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
    return JsonResponse({'error': 'Invalid request'}, status=400)
    
    
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Create your views here.

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.query_params.get('search', None)
        category = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) |
                Q(category__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category__icontains=category)
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            user_data = UserSerializer(user).data
            return Response({
                'message': 'User created successfully',
                'user': user_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        user_data = UserSerializer(user).data
        return Response({
            'message': 'Login successful',
            'user': user_data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user_data = UserSerializer(request.user).data
    return Response({'user': user_data}, status=status.HTTP_200_OK)

# Chat-related views

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def chat_sessions(request):
    if request.method == 'GET':
        sessions = ChatSession.objects.filter(user=request.user)
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create new chat session
        session_id = str(uuid.uuid4())
        session = ChatSession.objects.create(
            user=request.user,
            session_id=session_id
        )
        
        # Create welcome message
        chatbot = ChatbotService()
        welcome_response, _ = chatbot.generate_response("hello", request.user)
        
        ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=welcome_response
        )
        
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def chat_session_detail(request, session_id):
    try:
        session = ChatSession.objects.get(session_id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        session.delete()
        return Response({'message': 'Session deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def chat_messages(request, session_id):
    try:
        session = ChatSession.objects.get(session_id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        messages = session.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ChatMessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Save user message
            user_message = ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=serializer.validated_data['content']
            )
            
            # Generate bot response
            chatbot = ChatbotService()
            bot_response, related_products = chatbot.generate_response(
                serializer.validated_data['content'], 
                request.user
            )
            
            # Save bot message
            bot_message = ChatMessage.objects.create(
                session=session,
                message_type='bot',
                content=bot_response
            )
            
            # Add related products if any
            if related_products:
                bot_message.related_products.set(related_products)
            
            # Update session timestamp
            session.updated_at = timezone.now()
            session.save()
            
            # Return both messages
            user_data = ChatMessageSerializer(user_message).data
            bot_data = ChatMessageSerializer(bot_message).data
            
            return Response({
                'user_message': user_data,
                'bot_message': bot_data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def reset_chat_session(request, session_id):
    try:
        session = ChatSession.objects.get(session_id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Delete all messages in the session
    session.messages.all().delete()
    
    # Create new welcome message
    chatbot = ChatbotService()
    welcome_response, _ = chatbot.generate_response("hello", request.user)
    
    ChatMessage.objects.create(
        session=session,
        message_type='bot',
        content=welcome_response
    )
    
    return Response({'message': 'Chat session reset successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def product_search(request):
    serializer = ProductSearchSerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data.get('query', '')
        category = serializer.validated_data.get('category')
        min_price = serializer.validated_data.get('min_price')
        max_price = serializer.validated_data.get('max_price')
        min_rating = serializer.validated_data.get('min_rating')
        in_stock_only = serializer.validated_data.get('in_stock_only', True)
        
        # Build search query
        products = Product.objects.all()
        
        if query:
            products = products.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
        
        if category:
            products = products.filter(category__icontains=category)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
        
        if min_rating:
            products = products.filter(rating__gte=min_rating)
        
        if in_stock_only:
            products = products.filter(stock__gt=0)
        
        products = products[:20]  # Limit results
        serializer = ProductSerializer(products, many=True)
        
        return Response({
            'count': len(products),
            'results': serializer.data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




