from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UsersViewSet, PostsViewSet

router = DefaultRouter()
router.register("users", UsersViewSet, basename="users")
router.register("posts", PostsViewSet, basename="posts")

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
]
