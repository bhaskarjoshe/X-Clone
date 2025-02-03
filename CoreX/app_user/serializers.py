from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "profile_picture",
            "bio",
            "is_power_user",
            "last_login",
            "date_joined",
        ]
        read_only_fields = ["id", "username", "email", "last_login", "date_joined"]
