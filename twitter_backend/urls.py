from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import AuthViewSet, ProfileViewSet
from tweets.views import TweetViewSet
from direct_messages.views import ConversationViewSet, MessageViewSet
from notifications.views import send_notification
router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'tweets', TweetViewSet, basename='tweet')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/notifications/send/', send_notification, name='send_notification'),  # URL for the send_notification
] 
