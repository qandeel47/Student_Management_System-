from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Read-only representation of a user (used for nested display)."""

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "role", "phone", "address", "profile_picture",
            "is_active", "created_at",
        ]
        read_only_fields = fields


class AdminCreateUserSerializer(serializers.ModelSerializer):
    """
    Used only by Admin to create a new login account (for a teacher or student).
    Password is hashed properly via create_user().
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "password", "role", "phone", "address",
        ]

    def validate_role(self, value):
        if value == User.Role.ADMIN:
            raise serializers.ValidationError("Cannot create another admin account through this endpoint.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MyProfileSerializer(serializers.ModelSerializer):
    """Used by a logged-in user to view/update their own basic contact info."""

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "role", "phone", "address", "profile_picture",
        ]
        read_only_fields = ["id", "username", "role"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
