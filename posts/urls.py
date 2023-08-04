from django.urls import path

from .views import CreatePostView, DeletePostView

app_name = "posts"

urlpatterns = [
    path("create/", CreatePostView.as_view(), name="create"),
    path("<int:pk>/delete/", DeletePostView.as_view(), name="delete"),
]
