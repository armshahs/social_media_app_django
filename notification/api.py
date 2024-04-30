from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

from account.models import User

from .serializers import NotificationSerializer
from .models import Notification


@api_view(["GET"])
def notifications(request):
    received_notifications = request.user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(received_notifications, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def read_notification(request, pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()
    serializer = NotificationSerializer(notification)
    return Response(
        {
            "message": "Notification updated to read",
            "Notification details": serializer.data,
        }
    )
