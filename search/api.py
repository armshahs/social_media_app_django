from account.models import User
from django.db.models import Q
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)


# search from among the users and all posts on the search page
@api_view(["POST"])
def search(request):
    data = request.data
    query = data["query"]

    # get list of all uuids to filter posts (friends & self)
    friends = request.user.friends.all()
    created_by_ids = list(friends.values_list("id", flat=True))
    created_by_ids.append(request.user.id)

    users = User.objects.filter(name__icontains=query)
    users_serializer = UserSerializer(users, many=True)

    # filtering that either posts are from a friend or they are public posts by a stranger
    posts = Post.objects.filter(
        Q(body__icontains=query, is_private=False)
        | Q(created_by_id__in=created_by_ids, body__icontains=query)
    )
    posts_serializer = PostSerializer(posts, many=True)

    return Response({"users": users_serializer.data, "posts": posts_serializer.data})

    # get list of all uuids to filter posts (friends & self)
    friends = request.user.friends.all()
    created_by_ids = list(friends.values_list("id", flat=True))
    created_by_ids.append(request.user.id)

    # filter posts by uuids obtained above & also by "trends" queryparam
    posts = Post.objects.filter(created_by_id__in=created_by_ids)
