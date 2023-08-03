from rest_framework import serializers


class NotFoundResponse(serializers.Serializer):
    detail = serializers.CharField(default="Not found.")


class ForbiddenResponse(serializers.Serializer):
    detail = serializers.CharField(
        default="Authentication credentials were not provided."
    )
