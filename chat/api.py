from account.models import User
from rest_framework.generics import ListAPIView
from account.serializers import UserSerializer
from .models import Conversation, ConversationMessage
from .serializers import (
    ConversationSerializer,
    ConversationDetailSerializer,
    ConversationMessageSerializer,
)

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)


@api_view(["GET"])
def conversation_list(request):
    # We need conversations only where we are a part of it.
    conversations = Conversation.objects.filter(users__in=list([request.user]))

    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def conversation_detail(request, pk):
    # first filter if you are an owner, and then only get the conversation by pk.
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(
        pk=pk
    )
    serializer = ConversationDetailSerializer(conversation)

    return Response(serializer.data)


# Rewriting the above code (conversation_detail) in ListAPIView
class ConversationDetailView(ListAPIView):
    serializer_class = ConversationDetailSerializer

    def get_queryset(self):
        # fetch the pk value
        pk = self.kwargs["pk"]
        return Conversation.objects.filter(users__in=list([self.request.user])).filter(
            pk=pk
        )


@api_view(["GET"])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)
    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(
        users__in=list([user])
    )

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)

    return Response(serializer.data)


@api_view(["POST"])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(
        pk=pk
    )

    body = request.data.get("body")

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    if body:
        conversation_message = ConversationMessage.objects.create(
            body=body,
            conversation=conversation,
            created_by=request.user,
            sent_to=sent_to,
        )

        serializer = ConversationMessageSerializer(conversation_message)

        return Response(serializer.data)
    return Response({"The body is missing"})
