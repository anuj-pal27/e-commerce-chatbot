from django.urls import path
from . import views

urlpatterns = [
    # Product endpoints
    path('api/products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('api/products/<int:pk>/', views.ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('api/products/search/', views.product_search, name='product-search'),
    
    # Authentication endpoints
    path('api/auth/signup/', views.UserRegistrationView.as_view(), name='user-signup'),
    path('api/auth/login/', views.user_login, name='user-login'),
    path('api/auth/logout/', views.user_logout, name='user-logout'),
    path('api/auth/profile/', views.user_profile, name='user-profile'),
    
    # Chat endpoints
    path('api/chat/sessions/', views.chat_sessions, name='chat-sessions'),
    path('api/chat/sessions/<str:session_id>/', views.chat_session_detail, name='chat-session-detail'),
    path('api/chat/sessions/<str:session_id>/messages/', views.chat_messages, name='chat-messages'),
    path('api/chat/sessions/<str:session_id>/reset/', views.reset_chat_session, name='reset-chat-session'),
] 