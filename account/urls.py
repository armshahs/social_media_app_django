from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import api, views

urlpatterns = [
    path("me/", api.me, name="signup"),
    path("signup/", api.signup, name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("editprofile/", api.editprofile, name="editprofile"),
    path("edit_password/", api.edit_password, name="edit_password"),
    path("friends/suggested/", api.suggested_friends, name="suggested_friends"),
    # uuid of created_for = request.user
    path("friends/<uuid:pk>/", api.friends, name="friends"),
    # uuid of created_for
    path(
        "friends/<uuid:pk>/request/",
        api.send_friend_request,
        name="send_friend_request",
    ),
    # uuid of created_by
    path("friends/<uuid:pk>/<str:status>/", api.handle_request, name="handle_request"),
    path("activateemail/", views.activateemail, name="activateemail"),
]
