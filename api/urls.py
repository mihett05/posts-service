from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, PostsViewSet

router = DefaultRouter()
router.register("users", UsersViewSet, basename="users")
router.register("posts", PostsViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
]

print(router.urls)
