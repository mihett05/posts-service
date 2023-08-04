from rest_framework import serializers


class NotFoundResponse(serializers.Serializer):  # Для openapi
    detail = serializers.CharField(default="Not found.")


class ForbiddenResponse(serializers.Serializer):  # Для openapi
    detail = serializers.CharField(
        default="Authentication credentials were not provided."
    )
