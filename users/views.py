from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import HttpResponseRedirect, resolve_url
from django.contrib.auth import login
from django.conf import settings

from .serializers import UserSerializer


class RegisterView(APIView):
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
