from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture', 'email']

class FollowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="follower.username")

    class Meta:
        model = Follow
        fields = ["id", "username"]


class FollowingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="followed.username")

    class Meta:
        model = Follow
        fields = ["id", "username"]


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


