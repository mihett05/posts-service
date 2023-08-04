from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegisterView, UsersList, UserPostsView

app_name = "users"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("", UsersList.as_view(), name="list"),
    path("<int:pk>/posts/", UserPostsView.as_view(), name="posts"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
