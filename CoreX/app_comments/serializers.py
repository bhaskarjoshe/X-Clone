from rest_framework import serializers
from app_tweets.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "tweet",
            "author",
            "parent",
            "comment_content",
            "created_at",
            "is_deleted",
            "replies",
        ]

    def get_replies(self, obj):
        replies = obj.replies.filter(is_deleted=False).order_by('-created_at')
        return CommentSerializer(replies, many=True).data
