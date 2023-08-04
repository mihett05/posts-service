from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.serializers import UserSerializer
from posts.serializers import PostSerializer
from posts.models import Post
from posts.permissions import IsPostOwner

from .serializers import (
    NotFoundResponse,
    ForbiddenResponse,
)

User = get_user_model()


@extend_schema_view(
    create=extend_schema(
        description="Регистрация пользовтеля",
        responses={
            201: TokenObtainPairSerializer,
        },
    ),
    list=extend_schema(description="Получение списка пользователей"),
)
class UsersViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs).data
        user = User.objects.get(id=data["id"])
        token = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(token.access_token),
                "refresh": str(token),
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses={
            200: PostSerializer(many=True),
            404: NotFoundResponse,
        }
    )
    @action(
        detail=True,
        methods=["get"],
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

    @extend_schema(responses={200: UserSerializer})
    @action(detail=False)
    def me(self, request):
        return Response(self.get_serializer(instance=request.user).data)


@extend_schema_view(
    create=extend_schema(
        description="Создание поста",
        responses={403: ForbiddenResponse},
    ),
    destroy=extend_schema(
        description="Удаление пота",
        responses={403: ForbiddenResponse, 404: NotFoundResponse},
    ),
)
class PostsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsPostOwner]
