from rest_framework import serializers

from account.models import User

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "body",
            "type_of_notification",
            "post",
            # "post_id",  # just to check
            "created_by",
            "created_for",
            "created_at_formatted",
        )
