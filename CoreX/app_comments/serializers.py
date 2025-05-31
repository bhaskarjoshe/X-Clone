from app_tweets.models import Comment
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "profile_picture",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="author", write_only=True
    )
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), source="parent", allow_null=True, required=False
    )
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "tweet",
            "author",
            "author_id",
            "parent",
            "parent_id",
            "comment_content",
            "created_at",
            "is_deleted",
            "replies",
        ]

    def get_replies(self, obj):
        replies = obj.replies.filter(is_deleted=False).order_by("-created_at")
        return CommentSerializer(replies, many=True).data
