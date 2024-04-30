from .models import Post, PostAttachment, Comment, Trend
from rest_framework import serializers
from account.serializers import UserSerializer


class PostAttachmentSerializer(serializers.Serializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = PostAttachment
        fields = (
            "id",
            "get_image",
            "created_by",
        )


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "body",
            "created_by",
            "created_at_formatted",
        )


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "created_by",
            "created_at_formatted",
            "likes_count",
            "comments_count",
            "attachments",
            "is_private",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "created_by",
            "created_at_formatted",
            "likes_count",
            "comments",
            "comments_count",
            "attachments",
            "is_private",
        )


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = (
            "id",
            "hashtag",
            "occurences",
        )
