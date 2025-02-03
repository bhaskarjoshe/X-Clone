from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Follow
from .serializers import FollowerSerializer, FollowingSerializer

User = get_user_model()

class FollowerUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow == request.user:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Follow.objects.filter(follower=request.user, followed=user_to_follow).exists():
            return Response({"error": "Already following this user"}, status=status.HTTP_400_BAD_REQUEST)
        
        Follow.objects.create(follower=request.user, followed=user_to_follow)
        return Response({"message":f"You are now following {user_to_follow.username}"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        if not Follow.objects.filter(follower=request.user, followed=user_to_unfollow).exists():
            return Response({'error': "You are not following this user"}, status=status.HTTP_400_BAD_REQUEST)
    
        Follow.objects.filter(follower=request.user, followed=UserWarning).delete()
        return Response({"message":f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_204_NO_CONTENT)
    
class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following = Follow.objects.filter(follower=request.user)
        serializer = FollowingSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FollowerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followers = Follow.objects.filter(followed=request.user)
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)