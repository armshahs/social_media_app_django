from django.shortcuts import render
from django.db.models import Q
from account.models import User, FriendRequest
from notification.utils import create_notification
from account.serializers import UserSerializer
from .models import Post, PostAttachment, Like, Comment, Trend
from .serializers import (
    PostSerializer,
    PostDetailSerializer,
    CommentSerializer,
    TrendSerializer,
)
from .pagination import PostPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from .forms import PostForm, AttachmentForm

# Create your views here.


@api_view(["GET"])
def post_detail(request, pk):
    # get list of all uuids to filter posts (friends & self)
    friends = request.user.friends.all()
    created_by_ids = list(friends.values_list("id", flat=True))
    created_by_ids.append(request.user.id)

    # filter posts by uuids obtained above
    post = Post.objects.filter(
        Q(created_by_id__in=created_by_ids) | Q(is_private=False)
    ).get(pk=pk)

    serializer = PostDetailSerializer(post)
    return Response(serializer.data)


@api_view(["GET"])
def post_list(request):

    # get list of all uuids to filter posts (friends & self)
    friends = request.user.friends.all()
    created_by_ids = list(friends.values_list("id", flat=True))
    created_by_ids.append(request.user.id)

    # filter posts by uuids obtained above & also by "trends" queryparam
    posts = Post.objects.filter(created_by_id__in=created_by_ids)

    trend = request.GET.get("trend", "")  # default value is empty

    if trend:
        posts = posts.filter(body__icontains="#" + trend).filter(is_private=False)

    # pagination. Refer pagination.py file
    paginator = PostPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(paginated_posts, many=True)

    # return Response({"data": serializer.data})
    # changed to paginated response, hence commented the above line
    return paginator.get_paginated_response({"data": serializer.data})


# Rewriting the above function using Generic API View
class PostListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["body", "created_by__name", "created_by__email"]
    search_fields = ["body", "created_by__name", "created_by__email"]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # overriding the default queryset
    def get_queryset(self):
        friends = self.request.user.friends.all()
        created_by_ids = list(friends.values_list("id", flat=True))
        created_by_ids.append(self.request.user.id)

        # filtering by trend as well
        posts = self.queryset.filter(created_by_id__in=created_by_ids)
        trend = self.request.GET.get("trend", "")  # default is empty
        if trend:
            return posts.filter(body__icontains="#" + trend).filter(is_private=False)
        return posts


@api_view(["GET"])
def post_list_profile(request, id):

    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    # filtering for private posts. Only public should be visible for non-friends
    if not request.user in user.friends.all():
        posts = posts.filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendrequest = True

    # if already friends, then cannot send request
    if request.user in user.friends.all():
        can_send_friendrequest = False

    # if friend request already sent by either user/request.user, then cannot send request
    check1 = FriendRequest.objects.filter(created_for=request.user).filter(
        created_by=user
    )
    check2 = FriendRequest.objects.filter(created_for=user).filter(
        created_by=request.user
    )

    if check1 or check2:
        can_send_friendrequest = False

    return Response(
        {
            "user": user_serializer.data,
            "posts": posts_serializer.data,
            "can_send_friendrequest": can_send_friendrequest,
        }
    )


@api_view(["POST"])
def post_create(request):
    # since frontend is sending a formdata, we need to use request.POST
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    # print(attachment_form)
    # print(attachment)
    # print(request.POST)
    # print(request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()
        print(attachment)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count += 1
        user.save()

        serializer = PostSerializer(post)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["POST"])
def post_like(request, pk):

    # if user has already liked the post, then cannot do it again.
    post = Post.objects.get(pk=pk)
    check1 = post.likes.filter(created_by=request.user)

    if not check1:
        like = Like.objects.create(created_by=request.user)
        post.likes_count += 1
        # many to many field does not have an append method
        post.likes.add(like)
        post.save()

        # creating notification of liking the post
        notification = create_notification(request, "post_like", post_id=post.id)

        return Response({"The post was liked"})
    return Response({"message": "The post is already liked"})


@api_view(["POST"])
def post_create_comment(request, pk):
    comment = Comment.objects.create(
        body=request.data.get("body"), created_by=request.user
    )

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    # ceate a notification on adding a comment
    notification = create_notification(request, "post_comment", post_id=post.id)

    serializer = CommentSerializer(comment)

    return Response(serializer.data)


@api_view(["DELETE"])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()
    return Response({"message": "Post successfully deleted"})


@api_view(["POST"])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()
    return Response({"message": "Post reported"})


@api_view(["GET"])
def get_trends(request):
    trends = Trend.objects.all()
    seriallizer = TrendSerializer(trends, many=True)
    return Response(seriallizer.data)
