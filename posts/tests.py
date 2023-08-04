from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from .models import Post

User = get_user_model()


class PostsTest(APITestCase):
    user: User
    post = {"title": "Post title", "body": "Post body"}

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="user1", email="user1@example.com")
        cls.user.set_password("P@a$sw0rd")
        cls.user.save()

    def test_create_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("api:posts-list"), self.post).json()
        self.assertEquals(
            response["user"],
            self.user.username,
            "Post author is current user",
        )
        self.assertEquals(
            response["title"],
            self.post["title"],
            "Post has same title",
        )
        self.assertEquals(
            response["body"],
            self.post["body"],
            "Post has same body",
        )

    def test_create_post_unauthorized(self):
        self.assertNotEquals(
            self.client.post(reverse("api:posts-list"), self.post).status_code,
            201,
            "Can't create post when unauthorized",
        )

    def test_delete_post(self):
        self.client.force_login(self.user)
        post = Post.objects.create(**self.post, user=self.user)
        response = self.client.delete(
            reverse("api:posts-detail", kwargs={"pk": post.id})
        )
        self.assertEquals(
            response.status_code,
            204,
            "Delete should return 204 No content",
        )
        self.assertEquals(
            self.client.get(
                reverse("api:users-posts", kwargs={"pk": self.user.id})
            ).json(),
            [],
            "Posts should be empty list after delete",
        )

    def test_delete_post_unauthorized(self):
        post = Post.objects.create(**self.post, user=self.user)
        self.assertNotEquals(
            self.client.delete(reverse("api:posts-detail", kwargs={"pk": post.id})),
            204,
            "Can't remove posts when unauthorized",
        )

    def test_delete_another_post(self):
        self.client.force_login(self.user)

        another_user = User.objects.create(
            **{"username": "user2", "email": "user2@example.com"}
        )
        another_user.set_password("P@a$sw0rd")
        another_user.save()
        another_post = Post.objects.create(**self.post, user=another_user)

        self.assertNotEquals(
            self.client.delete(
                reverse("api:posts-detail", kwargs={"pk": another_post.id})
            ).status_code,
            204,
            "Can't remove another users posts",
        )
