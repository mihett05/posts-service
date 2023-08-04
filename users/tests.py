from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

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
            title="Example title",
            body="Example body",
            user=cls.user,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_users_list(self):
        response = self.client.get(reverse("api:users-list")).json()
        self.assertEquals(len(response), 1, "Same users count")
        self.assertEquals(response[0]["id"], self.user.id, "Same user id")
        self.assertEquals(
            response[0]["username"], self.user.username, "Same user username"
        )
        self.assertEquals(response[0]["email"], self.user.email, "Same user email")

    def test_users_posts(self):
        response = self.client.get(
            reverse("api:users-posts", args=[self.user.id])
        ).json()
        self.assertEquals(len(response), 1, "Same posts count")
        self.assertEquals(response[0]["id"], self.post.id, "Same post id")
        self.assertEquals(
            response[0]["user"], self.post.user.username, "Same post author"
        )
        self.assertEquals(response[0]["title"], self.post.title, "Same post title")
        self.assertEquals(response[0]["body"], self.post.body, "Same post body")
