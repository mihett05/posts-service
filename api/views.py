from rest_framework import viewsets, mixins, serializers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, inline_serializer, extend_schema_view

from users.serializers import UserSerializer
from posts.serializers import PostSerializer

from posts.models import Post
from .serializers import (
    NotFoundResponse,
    ForbiddenResponse,
)

User = get_user_model()


class UsersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        responses={
            200: PostSerializer(many=True),
            404: NotFoundResponse,
        }
    )
    @action(
        detail=True,
        methods=["get"],
        name="Get user's posts",
        url_path="posts",
        url_name="posts",
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


@extend_schema_view(
    create=extend_schema(responses={403: ForbiddenResponse}),
    destroy=extend_schema(responses={403: ForbiddenResponse, 404: NotFoundResponse}),
)
class PostsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
