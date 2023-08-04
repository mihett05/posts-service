from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from django.shortcuts import HttpResponseRedirect, resolve_url
from django.contrib.auth import login, get_user_model
from django.conf import settings

from .serializers import UserSerializer, UserPostsSerializer

User = get_user_model()


class RegisterView(views.APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "users/register.html"

    def get(self, request):
        serializer = UserSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = UserSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response({"serializer": serializer})
        user = serializer.save()
        login(request, user)
        return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))


class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "users/list.html"

    def get(self, request, *args, **kwargs):
        users = self.filter_queryset(self.get_queryset())
        rows = [
            users[i : i + 3] for i in range(0, len(users), 3)
        ]  # разбить юзеров на ряды по 3 в каждом
        return Response({"rows": rows})


class UserPostsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPostsSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "users/posts.html"
