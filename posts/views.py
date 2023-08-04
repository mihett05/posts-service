from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import HttpResponseRedirect, reverse

from .models import Post
from .serializers import PostSerializer
from .permissions import IsPostOwner


class DeletePostView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsPostOwner]

    def post(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return HttpResponseRedirect(
            reverse("users:posts", kwargs={"pk": request.user.id}),
            status=status.HTTP_204_NO_CONTENT,
        )


class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "posts/create.html"

    def get(self, request, *args, **kwargs):
        serializer = PostSerializer()
        return Response({"serializer": serializer})

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return HttpResponseRedirect(
            reverse(
                "users:posts",
                kwargs={"pk": request.user.id},
            ),
            status=status.HTTP_201_CREATED,
        )
