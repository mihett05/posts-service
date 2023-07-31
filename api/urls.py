from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, PostsViewSet

router = DefaultRouter()
router.register("users", UsersViewSet, basename="user")
router.register("posts", PostsViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
