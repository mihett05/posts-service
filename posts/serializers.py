from rest_framework import serializers
from .models import Post


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
