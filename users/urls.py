from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter

from .views import RegisterView, UsersList, UserPostsView

app_name = "users"

# router = DefaultRouter()
# router.register("", UsersViewSet, basename="users")

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("", UsersList.as_view(), name="list"),
    path("<int:pk>/posts/", UserPostsView.as_view(), name="posts"),
]
