from rest_framework import viewsets, mixins, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, inline_serializer

from posts.models import Post
from .serializers import UserSerializer, PostSerializer
from .permissions import IsPostOwnerOrReadOnly

User = get_user_model()


class UsersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        responses={
            200: PostSerializer(many=True),
            404: inline_serializer(
                name="NotFoundResponse",
                fields={"detail": serializers.CharField(default="Not found.")},
            ),
        }
    )
    @action(
        detail=True,
        methods=["get"],
        name="Get user's posts",
        url_path="posts",
        url_name="User's posts",
    )
    def posts(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        return Response(
            PostSerializer(
                instance=Post.objects.filter(user=user).all(),
                many=True,
                context=self.get_serializer_context(),
            ).data
        )


class PostsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsPostOwnerOrReadOnly,)
