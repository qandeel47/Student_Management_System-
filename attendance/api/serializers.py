from django.db import IntegrityError
from rest_framework import serializers

from courses.models import Course
from students.models import Student
from ..models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    """Full representation used for listing/retrieving (admin & teacher)."""

    student_roll_number = serializers.CharField(source="student.roll_number", read_only=True)
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    course_code = serializers.CharField(source="course.code", read_only=True)
    marked_by_name = serializers.CharField(source="marked_by.user.get_full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id", "student", "student_roll_number", "student_name",
            "course", "course_code", "marked_by", "marked_by_name",
            "date", "status", "remarks", "created_at",
        ]
        read_only_fields = ["marked_by", "created_at"]


class MarkAttendanceSerializer(serializers.ModelSerializer):
    """
    Used by a Teacher to mark attendance for a student in one of their own courses.
    'marked_by' is set automatically from the logged-in teacher, never from client input.
    """

    class Meta:
        model = Attendance
        fields = ["id", "student", "course", "date", "status", "remarks"]

    def validate_course(self, course):
        request = self.context["request"]
        teacher = request.user.teacher_profile
        if course.teacher_id != teacher.id:
            raise serializers.ValidationError("You can only mark attendance for your own courses.")
        return course

    def validate_student(self, student):
        return student

    def validate(self, attrs):
        course = attrs.get("course")
        student = attrs.get("student")
        if course and student and not student.courses.filter(id=course.id).exists():
            raise serializers.ValidationError(
                {"student": "This student is not enrolled in the selected course."}
            )
        return attrs

    def create(self, validated_data):
        teacher = self.context["request"].user.teacher_profile
        validated_data["marked_by"] = teacher
        try:
            return Attendance.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Attendance for this student, course, and date has already been marked. "
                "Update the existing record instead."
            )


class MyAttendanceSerializer(serializers.ModelSerializer):
    """Read-only view for a student checking their own attendance."""

    course_code = serializers.CharField(source="course.code", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "course", "course_code", "course_name", "date", "status", "remarks"]
        read_only_fields = fields
