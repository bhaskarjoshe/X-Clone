from rest_framework import serializers
from app_tweets.models import Like, Tweet
from django.contrib.auth import get_user_model

User = get_user_model()

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id', 'tweet_content', 'author', 'created_at', 'updated_at', 'is_pinned', 'is_deleted']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    tweet = TweetSerializer()
    
    class Meta:
        model= Like
        fields = ['id', 'user', 'tweet', 'created_at']