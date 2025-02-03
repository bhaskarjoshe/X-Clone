from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from app_tweets.models import Tweet, Like
from app_likes.serializers import LikeSerializer

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

    def post(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        like = Like.objects.filter(tweet=tweet, user=request.user).first()
        if not like:
            return Response({
                "detail": "You have not liked this tweet."
            }, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({"detail": "Like removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class GetLikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        likes = Like.objects.filter(tweet=tweet)
        if not likes.exists():
            return Response(
                {"detail": "no likes found for this tweet."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)