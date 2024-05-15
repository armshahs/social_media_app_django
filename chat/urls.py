from django.urls import path

from . import api

urlpatterns = [
    path("", api.conversation_list, name="conversation_list"),
    # rewriting the above url using related names on User model
    path("conversation_list_2", api.conversation_list_2, name="conversation_list_2"),
    path("<uuid:pk>/", api.conversation_detail, name="conversation_detail"),
    # Same as above with ListAPIView
    path(
        "<uuid:pk>/view/",
        api.ConversationDetailView.as_view(),
        name="ConversationDetailView",
    ),
    path(
        "<uuid:pk>/send/",
        api.conversation_send_message,
        name="conversation_send_message",
    ),
    path(
        "<uuid:user_pk>/get-or-create/",
        api.conversation_get_or_create,
        name="conversation_get_or_create",
    ),
]
