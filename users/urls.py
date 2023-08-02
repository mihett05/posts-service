from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegisterView

app_name = "users"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("register/", RegisterView.as_view(), name="register"),
]
