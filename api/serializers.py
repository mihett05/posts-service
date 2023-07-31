from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "date_joined"]

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


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField(
        many=False,
        slug_field="username",
        read_only=True,
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "user", "title", "body", "created_at", "updated_at"]

    def create(self, validated_data):
        # Получить пользователя из запроса и назначить его автором поста
        user = self.context["request"].user
        post = Post.objects.create(
            user=user,
            **validated_data,
        )
        post.save()
        return post
