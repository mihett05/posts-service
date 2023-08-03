from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, validators
from django.contrib.auth import get_user_model, password_validation

from posts.serializers import PostSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        label=_("Username"),
        style={"input_type": "text"},
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message="Имя пользователя уже используется",
            )
        ],
    )
    email = serializers.EmailField(
        label=_("Email"),
        style={"input_type": "email"},
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message="Адрес электронной почты уже используется",
            )
        ],
    )
    password = serializers.CharField(
        label=_("Password"),
        write_only=True,
        style={"input_type": "password"},
        required=True,
    )
    password_again = serializers.CharField(
        label="Повторите пароль",
        write_only=True,
        style={"input_type": "password"},
        required=True,
    )
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        model_fields = ["id", "username", "email", "password", "date_joined"]
        extra_fields = ["password_again"]
        fields = model_fields + extra_fields

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate_password_again(self, value):
        if (
            "password" not in self.initial_data
            or value != self.initial_data["password"]
        ):
            raise validators.ValidationError("Пароли должны совпадать")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key != "password":
                setattr(instance, key, value)
            else:
                instance.set_password(validated_data["password"])
        instance.save()


class UserPostsSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "posts"]
