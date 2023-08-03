from django.urls import path, include

app_name = "posts"

urlpatterns = [
    path("user/<id:user_id>/"),
]
