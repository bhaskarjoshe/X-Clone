from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Tweet, Comment, Like, Media
from .tasks import fetch_tweets_async
from .serializers import (
    TweetSerializer,
    LikeSerializer,
    CommentSerializer,
    MediaSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser


class TweetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UserTweetsByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TweetPagination()

    def get(self, request, user_id):
        tweets = Tweet.objects.filter(author_id=user_id, is_deleted=False).order_by(
            "-created_at"
        )

        if not tweets.exists():
            return Response(
                {"detail": "No tweets found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        paginator = self.pagination_class
        result_page = paginator.paginate_queryset(tweets, request)
        serializer = TweetSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class TweetListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        if request.user.is_power_user:
            tweets = Tweet.objects.all().order_by("-created_at")
        else:
            tweets = Tweet.objects.filter(
                author=request.user, is_deleted=False
            ).order_by("-created_at")

        paginator = TweetPagination()
        result_page = paginator.paginate_queryset(tweets, request, view=self)
        serializer = TweetSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        media_files = request.FILES.getlist("media")
        serializer = TweetSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            tweet = serializer.save()
            media_instances = [Media.objects.create(file=file) for file in media_files]
            tweet.media.set(media_instances)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class allTweetView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TweetPagination()

    def get(self, request):
        tweets = Tweet.objects.filter(is_deleted=False).order_by("-created_at")
        paginator = self.pagination_class
        result_page = paginator.paginate_queryset(tweets, request)
        serializer = TweetSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FollowingTweetsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TweetPagination()

    def get(self, request):
        user = request.user
        following_users = user.following.values_list("followed", flat=True)
        tweets = Tweet.objects.filter(
            author_id__in=following_users, is_deleted=False
        ).order_by("-created_at")

        paginator = self.pagination_class
        result_page = paginator.paginate_queryset(tweets, request)
        serializer = TweetSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


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
        request.data["created_at"] = timezone.now()

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


class UnlikeTweetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)

        like = Like.objects.filter(tweet=tweet, user=request.user).first()
        if not like:
            return Response(
                {"detail": "You have not liked this tweet."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like.delete()
        return Response(
            {"detail": "Like removed from the tweet."},
            status=status.HTTP_204_NO_CONTENT,
        )


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


class UploadMediaView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):

        tweet = get_object_or_404(Tweet, pk=pk)

        if tweet.author != request.user:
            return Response(
                {"detail": "You can upload media to your own tweet"},
                status=status.HTTP_403_FORBIDDEN,
            )

        media_files = request.FILES.getlist("file")
        print(media_files)

        if not media_files:
            return Response(
                {"detail": "File is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        media_instances = [
            Media.objects.create(file=file) for file in media_files
        ]  # Create media first
        tweet.media.add(*media_instances)

        return Response(
            MediaSerializer(media_instances, many=True).data,
            status=status.HTTP_201_CREATED,
        )


class GetMediaByTweetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        media = Media.objects.filter(tweets=tweet)

        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data)


# celery
class FetchTweetsAsyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        result = fetch_tweets_async.delay(user_id)

        if isinstance(result, str) and result.startswith('{'):
            response = Response(result, content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="tweets_{user_id}.json"'
            return response

        return Response(
            {"detail": "Fetching tweets asynchronously.", "task_id": result.id},
            status=status.HTTP_202_ACCEPTED,
        )
