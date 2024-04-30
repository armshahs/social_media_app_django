from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from .forms import SignupForm, ProfileForm
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from django.contrib.auth.hashers import make_password
from notification.utils import create_notification


@api_view(["GET"])
def me(request):
    return Response(
        {
            "id": request.user.id,
            "name": request.user.name,
            "email": request.user.email,
            "avatar": request.user.get_avatar(),
        }
    )


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = "success"

    form = SignupForm(data)
    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()

        # email verification during signup
        url = (
            f"http://127.0.0.1:8000/api/activateemail/?email={user.email}&id={user.id}"
        )

        send_mail(
            "Please verify your email",
            f"In order to get activated, please verify your email at this url: {url}",
            "admin@shark.com",
            [user.email],
            fail_silently=False,
        )

        return Response({"message": message})
    else:
        return Response(form.errors)


@api_view(["GET"])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendRequest.objects.filter(
            created_for=request.user, status=FriendRequest.SENT
        )

    friends = user.friends.all()

    return Response(
        {
            "user": UserSerializer(user).data,
            "friends": UserSerializer(friends, many=True).data,
            "requests": FriendRequestSerializer(requests, many=True).data,
        }
    )


@api_view(["GET"])
def suggested_friends(request):
    user = request.user
    suggested_friends = user.suggested_friends.all()
    serializer = UserSerializer(suggested_friends, many=True)
    return Response({"user": request.user.email, "suggested firends": serializer.data})


@api_view(["POST"])
def editprofile(request):
    user = request.user
    email = request.data.get("email")

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return Response({"message": "Email already exists"})
    else:
        form = ProfileForm(request.data, request.FILES, instance=user)
        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)

        return Response({"message": "Information updated", "user": serializer.data})


@api_view(["POST"])
def edit_password(request):
    user = request.user

    form = PasswordChangeForm(data=request.data, user=user)

    if form.is_valid():
        form.save()
        return Response({"message": "Password reset successful"})
    return Response({"message": form.errors})


@api_view(["POST"])
def send_friend_request(request, pk):
    user = User.objects.get(id=pk)

    # should not already be friends, check if they are friends (not required since friendrequest will already be present for friends)
    # check0 = User.objects.filter(friends__icontains=user)
    # friend request should not already have been sent either by user or request.user
    check1 = FriendRequest.objects.filter(created_for=request.user, created_by=user)
    check2 = FriendRequest.objects.filter(created_for=user, created_by=request.user)

    if not check1 and not check2:
        friendrequest = FriendRequest.objects.create(
            created_for=user, created_by=request.user
        )

        notification = create_notification(
            request, "new_friendrequest", friendrequest_id=friendrequest.id
        )

        return Response({"message": "Request has been sent"})
    return Response({"message": "Friend request already sent"})


@api_view(["POST"])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)

    # update status of friend request
    friend_request = FriendRequest.objects.filter(created_for=request.user).get(
        created_by=user
    )
    friend_request.status = status
    friend_request.save()

    # update friends counter for user
    user.friends.add(request.user)
    user.friends_count += 1
    user.save()

    # update friends counter for request .user
    request_user = request.user
    request_user.friends_count += 1
    request_user.save()

    # sending notifications for accepted/rejected
    if status == "accepted":
        notification = create_notification(
            request, "accepted_friendrequest", friendrequest_id=friend_request.id
        )
    elif status == "rejected":
        notification = create_notification(
            request, "rejected_friendrequest", friendrequest_id=friend_request.id
        )

    return Response({"message": "Friendship request updated"})
