from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "profile_picture", "email"]


class FollowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="follower.username")
    follower_id = serializers.IntegerField(source="follower.id")
    email = serializers.EmailField(source="follower.email")
    is_power_user = serializers.BooleanField(source="followed.is_power_user")

    class Meta:
        model = Follow
        fields = ["id", "username", "follower_id", "email", "is_power_user"]


class FollowingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="followed.username")
    following_id = serializers.IntegerField(source="followed.id")
    email = serializers.EmailField(source="followed.email")
    is_power_user = serializers.BooleanField(source="followed.is_power_user")

    class Meta:
        model = Follow
        fields = ["id", "username", "following_id", "email", "is_power_user"]


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]
