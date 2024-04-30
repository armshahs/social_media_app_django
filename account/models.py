import uuid

from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


# Create your models here.
class CustomUserManager(UserManager):

    def _create_user(self, name, email, password, **extra_fields):

        if not email:
            raise ValueError("You have not provided a valid email address")

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True, default="default")
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    friends = models.ManyToManyField("self")
    friends_count = models.IntegerField(default=0)

    suggested_friends = models.ManyToManyField("self")

    posts_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email + str(self.id)

    # to get url of avatar image
    def get_avatar(self):
        if self.avatar:
            return "http://127.0.0.1:8000" + self.avatar.url
        else:
            return "https://i.pinimg.com/736x/0d/64/98/0d64989794b1a4c9d89bff571d3d5842.jpg"


class FriendRequest(models.Model):
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

    STATUS_CHOICES = (
        (SENT, "Sent"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(
        User, related_name="received_friendrequests", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name="created_friendrequests", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=SENT)

    class Meta:
        ordering = ("-created_at",)
