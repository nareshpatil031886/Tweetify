from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Tweet
from .serializers import TweetSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]  # Add this line to require authentication

    def perform_create(self, serializer):
        # This automatically sets the user to the current authenticated user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        tweet = self.get_object()
        if request.user in tweet.likes.all():
            tweet.likes.remove(request.user)
            return Response({'status': 'unliked'})
        tweet.likes.add(request.user)
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def retweet(self, request, pk=None):
        tweet = self.get_object()
        if request.user in tweet.retweets.all():
            tweet.retweets.remove(request.user)
            return Response({'status': 'unretweeted'})
        tweet.retweets.add(request.user)
        return Response({'status': 'retweeted'})
