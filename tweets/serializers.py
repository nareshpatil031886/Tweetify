from rest_framework import serializers
from .models import Tweet, Media, Bookmark
from accounts.serializers import UserSerializer

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'type', 'created_at']

class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    retweets_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_retweeted = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id', 
            'user', 
            'content', 
            'ai_description',
            'created_at', 
            'updated_at',
            'media',
            'likes_count',
            'retweets_count',
            'is_liked',
            'is_retweeted'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_retweets_count(self, obj):
        return obj.retweets.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_is_retweeted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.retweets.filter(id=request.user.id).exists()
        return False

class BookmarkSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'tweet', 'created_at']
