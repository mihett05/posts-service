from django.shortcuts import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()


class UsersTest(APITestCase):
    user: User
    post: Post

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="test_user",
            email="test_email@mail.com",
        )
        cls.user.set_password("P@a$sw0rd")
        cls.user.save()
        cls.post = Post.objects.create(
            title="Example title", body="Example body", user=cls.user
        )

    def test_users_list(self):
        response = self.client.get(reverse("users-list")).json()
        self.assertEquals(len(response), 1)
        self.assertEquals(response[0]["id"], self.user.id)
        self.assertEquals(response[0]["username"], self.user.username)
        self.assertEquals(response[0]["email"], self.user.email)

    def test_users_posts(self):
        response = self.client.get(reverse("users-posts", args=[self.user.id])).json()
        self.assertEquals(len(response), 1)
        self.assertEquals(response[0]["id"], self.post.id)
        self.assertEquals(response[0]["user"], self.post.user.username)
        self.assertEquals(response[0]["title"], self.post.title)
        self.assertEquals(response[0]["body"], self.post.body)
