from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated

from app_tweets.models import Tweet, Comment
from .serializers import CommentSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class CommentListView(APIView):
    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        comments = Comment.objects.filter(
            tweet=tweet, is_deleted=False, parent=None
        ).order_by("-created_at")

        page = request.GET.get("page", 1)
        paginator = Paginator(comments, 10)
        page_obj = paginator.get_page(page)

        serializer = CommentSerializer(page_obj, many=True)
        return Response(
            {"comments": serializer.data, "total_pages": paginator.num_pages},
            status=status.HTTP_200_OK,
        )


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        data = request.data

        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"Parent comment ID: {data.get('parent_id')}")
        author = request.user
        parent_comment = None

        if data.get("parent_id"):
            parent_comment = get_object_or_404(
                Comment, id=data["parent_id"], tweet=tweet
            )

        comment_content = data.get("comment_content")
        if not comment_content:
            return Response(
                {"error": "Comment content is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment = Comment.objects.create(
            tweet=tweet,
            author=author,
            parent=parent_comment,
            comment_content=comment_content,
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, is_deleted=False)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, is_deleted=False)
        data = request.data

        if comment.author.id != data.get("author_id"):
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        comment.comment_content = data.get("comment_content", comment.comment_content)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.author.id != request.user.id:
            return Response(
                {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        comment.is_deleted = True
        comment.save()
        return Response(
            {"message": "Comment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CommentRepliesView(APIView):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, is_deleted=False)
        replies = comment.replies.filter(is_deleted=False).order_by("-created_at")

        serializer = CommentSerializer(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, comment_id):
        parent_comment = get_object_or_404(Comment, id=comment_id, is_deleted=False)
        data = request.data

        comment_content = data.get("comment_content")
        if not comment_content:
            return Response({
                "error": "Comment content is required."
            }, status = status.HTTP_400_BAD_REQUEST)
        
        reply = Comment.objects.create(
            tweet = parent_comment.tweet,
            author=request.user,
            parent=parent_comment,
            comment_content=comment_content,
        )

        serializer = CommentSerializer(reply)
        return Response(serializer.data, status=status.HTTP_201_CREATED)