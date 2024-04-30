from django.db import models
import uuid
from account.models import User
from post.models import Post
from django.utils.timesince import timesince


# Create your models here.
class Notification(models.Model):

    NEW_FRIEND_REQUEST = "new_friendrequest"
    ACCEPTED_FRIEND_REQUEST = "accepted_friendrequest"
    REJECTED_FRIEND_REQUEST = "rejected_friendrequest"
    POST_LIKE = "post_like"
    POST_COMMENT = "post_comment"

    CHOICES_NOTIFICATION_TYPE = (
        (NEW_FRIEND_REQUEST, "New friend request"),
        (ACCEPTED_FRIEND_REQUEST, "Accepted friend request"),
        (POST_LIKE, "Post Liked"),
        (POST_COMMENT, "Post Comment"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(
        max_length=50, choices=CHOICES_NOTIFICATION_TYPE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name="created_notifications", on_delete=models.CASCADE
    )
    created_for = models.ForeignKey(
        User,
        related_name="received_notifications",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def created_at_formatted(self):
        return timesince(self.created_at)
