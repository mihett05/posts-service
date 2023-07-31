from rest_framework import viewsets
from django.contrib.auth import get_user_model

from posts.models import Post
from .serializers import UserSerializer, PostSerializer
from .permissions import IsCurrentUserOrReadOnly, IsPostOwnerOrReadOnly

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCurrentUserOrReadOnly,)


class PostsViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsPostOwnerOrReadOnly,)
