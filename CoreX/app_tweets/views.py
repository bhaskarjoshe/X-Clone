from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Tweet, Comment
from .serializers import TweetSerializer, LikeSerializer, CommentSerializer


class TweetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class TweetListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_power_user:
            tweets = Tweet.objects.all()
        else:
            tweets = Tweet.objects.filter(author=request.user, is_deleted=False)

        paginator = TweetPagination()
        result_page = paginator.paginate_queryset(tweets, request)
        serializer = TweetSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TweetSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TweetDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Tweet, pk=pk)

    def get(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.is_deleted:
            return Response(
                {"detail": "This tweet has been deleted"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)

    def delete(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.author != request.user:
            return Response(
                {"detail": "You can only delete your own tweets."},
                status=status.HTTP_403_FORBIDDEN,
            )
        tweet.is_deleted = True
        tweet.save()
        return Response(
            {"detail": "Tweet deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )

    def put(self, request, pk):
        tweet = self.get_object(pk)

        if tweet.author != request.user:
            return Response(
                {"detail": "You can only edit your own tweets."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not request.user.is_power_user:
            return Response(
                {"detail": "Only power users can edit tweets."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TweetSerializer(
            tweet, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PinTweetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        if not request.user.is_power_user:
            return Response(
                {"detail": "Only power users can pin tweets."},
                status=status.HTTP_403_FORBIDDEN,
            )
        tweet.is_pinned = True
        tweet.save()
        return Response(TweetSerializer(tweet).data)


class LikeTweetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        if Like.objects.filter(tweet=tweet, user=request.user).exists():
            return Response(
                {"detail": "You already liked this tweet."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        like = Like.objects.create(tweet=tweet, user=request.user)
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)


class GetLikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        likes = Like.objects.filter(tweet=tweet)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class CommentTweetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        comment_content = request.data.get("comment_content")
        if not comment_content:
            return Response(
                {"detail": "Content is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        comment = Comment.objects.create(
            tweet=tweet, author=request.user, comment_content=comment_content
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
