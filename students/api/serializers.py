from django.db import transaction
from rest_framework import serializers

from courses.models import Course
from courses.api.serializers import CourseSerializer
from users.models import User
from users.api.serializers import UserSerializer
from ..models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Read/list representation with nested user info (used by Admin)."""

    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    courses = CourseSerializer(many=True, read_only=True)
    course_ids = serializers.PrimaryKeyRelatedField(
        source="courses", queryset=Course.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = Student
        fields = [
            "id", "user", "roll_number", "department", "department_name",
            "courses", "course_ids", "semester", "date_of_birth", "admission_date",
            "guardian_name", "guardian_phone",
        ]


class AdminCreateStudentSerializer(serializers.ModelSerializer):
    """
    Admin creates a Student in one go: user login details + student profile fields.
    """

    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Student
        fields = [
            "id", "username", "email", "password", "first_name", "last_name", "phone",
            "roll_number", "department", "courses", "semester", "date_of_birth",
            "admission_date", "guardian_name", "guardian_phone",
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        courses = validated_data.pop("courses", [])
        user = User.objects.create_user(
            username=validated_data.pop("username"),
            email=validated_data.pop("email"),
            password=validated_data.pop("password"),
            first_name=validated_data.pop("first_name", ""),
            last_name=validated_data.pop("last_name", ""),
            phone=validated_data.pop("phone", ""),
            role=User.Role.STUDENT,
        )
        student = Student.objects.create(user=user, **validated_data)
        if courses:
            student.courses.set(courses)
        return student


class MyStudentProfileSerializer(serializers.ModelSerializer):
    """Read-only view for a student checking their own profile."""

    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            "id", "user", "roll_number", "department", "department_name",
            "courses", "semester", "date_of_birth", "admission_date",
            "guardian_name", "guardian_phone",
        ]
        read_only_fields = fields
