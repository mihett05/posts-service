from django.shortcuts import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


user_data = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "P@a$sw0rd",
}


class RegisterTest(APITestCase):
    user = user_data.copy()

    def create_user(self):
        user = User.objects.create(
            username=self.user["username"],
            email=self.user["email"],
        )
        user.set_password(self.user["password"])
        user.save()
        return user

    def register(self, data):
        return self.client.post(
            reverse("api:users-list"), {**data, "password_again": data["password"]}
        )

    def test_user_register(self):
        tokens = self.register(self.user).json()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(
            reverse("api:users-self"),
        ).json()
        self.assertEquals(
            response["username"],
            self.user["username"],
            "Token returns correct username",
        )
        self.assertEquals(
            response["email"], self.user["email"], "Token returns correct email"
        )

    def test_user_invalid_register(self):
        self.create_user()
        self.assertNotEquals(
            self.register(self.user).status_code,
            201,
            "Can't register existing user",
        )

        self.assertNotEquals(
            self.register(
                {
                    "username": self.user["username"],
                    "email": "random_email@example.com",
                    "password": self.user["password"],
                }
            ).status_code,
            201,
            "Can't register user with same username",
        )

        self.assertNotEquals(
            self.register(
                {
                    "username": "random_username",
                    "email": self.user["email"],
                    "password": self.user["password"],
                }
            ).status_code,
            201,
            "Can't register user with same email",
        )


class LoginTest(APITestCase):
    user = user_data.copy()

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username=cls.user["username"],
            email=cls.user["email"],
        )
        user.set_password(cls.user["password"])
        user.save()

    def login(self, data):
        return self.client.post(reverse("api:get_token"), data)

    def test_login(self):
        body = self.user.copy()
        body.pop("email")

        response = self.login(body)
        self.assertEquals(response.status_code, 200, "Login is performed correctly")
        tokens = response.json()
        self.assertTrue("access" in tokens, "Has access token")
        self.assertTrue("refresh" in tokens, "Has refresh token")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

        me = self.client.get(reverse("api:users-self")).json()
        self.assertEquals(me["username"], self.user["username"], "Same account")

    def test_invalid_login(self):
        self.assertNotEquals(
            self.login({"username": "random_user", "password": "password"}).status_code,
            200,
            "Can't login not existing user",
        )
        self.assertNotEquals(
            self.login(
                {
                    "username": self.user["username"],
                    "password": "password",
                }
            ).status_code,
            200,
            "Can't login with invalid password",
        )
