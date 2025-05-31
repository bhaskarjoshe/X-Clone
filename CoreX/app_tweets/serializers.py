from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment, Like, Media, Tweet

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_power_user"]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "file", "uploaded_at"]


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = ["id", "user", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "comment_content",
            "created_at",
            "is_deleted",
            "parent_id",
        ]


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    media = MediaSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False, read_only=True)
    likes = LikeSerializer(many=True, required=False)

    def get_like_count(self, current_tweet):
        return current_tweet.likes.count()

    class Meta:
        model = Tweet
        fields = [
            "id",
            "tweet_content",
            "author",
            "created_at",
            "updated_at",
            "is_pinned",
            "is_deleted",
            "likes",
            "media",
            "comments",
        ]

    def validate_tweet_content(self, value):
        user = self.context["request"].user
        if not user.is_power_user and len(value) > 280:
            raise serializers.ValidationError(
                "Tweet content exceeds the character limit for regular user."
            )
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user

        media_data = validated_data.pop("media", [])

        tweet = Tweet.objects.create(**validated_data)

        media_instances = [Media.objects.create(**media) for media in media_data]
        tweet.media.set(media_instances)

        return tweet
