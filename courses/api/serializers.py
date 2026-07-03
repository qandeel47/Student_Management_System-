from rest_framework import serializers

from ..models import Course


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "name", "code", "department", "department_name",
            "teacher", "teacher_name", "credit_hours", "description", "created_at",
        ]
