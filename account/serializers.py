from rest_framework import serializers

from .models import User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "friends_count",
            "posts_count",
            "get_avatar",
        )


class FriendRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = (
            "id",
            "created_for",
            "created_by",
            "status",
        )
