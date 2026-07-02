from django.db import transaction
from rest_framework import serializers

from departments.models import Department
from users.models import User
from users.serializers import UserSerializer
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    """Read/list representation with nested user info."""

    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Teacher
        fields = [
            "id", "user", "employee_id", "department", "department_name",
            "designation", "qualification", "date_of_joining",
        ]


class AdminCreateTeacherSerializer(serializers.ModelSerializer):
    """
    Admin creates a Teacher in one go: user login details + teacher profile fields.
    """

    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Teacher
        fields = [
            "id", "username", "email", "password", "first_name", "last_name", "phone",
            "employee_id", "department", "designation", "qualification", "date_of_joining",
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.pop("username"),
            email=validated_data.pop("email"),
            password=validated_data.pop("password"),
            first_name=validated_data.pop("first_name", ""),
            last_name=validated_data.pop("last_name", ""),
            phone=validated_data.pop("phone", ""),
            role=User.Role.TEACHER,
        )
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher


class MyTeacherProfileSerializer(serializers.ModelSerializer):
    """Read-only view for a teacher checking their own profile."""

    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Teacher
        fields = [
            "id", "user", "employee_id", "department", "department_name",
            "designation", "qualification", "date_of_joining",
        ]
        read_only_fields = fields
